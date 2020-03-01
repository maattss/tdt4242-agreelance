from django.http import HttpResponse, HttpResponseRedirect
from user.models import Profile
from .models import Project, Task, TaskFile, TaskOffer, Delivery, ProjectCategory, Team, TaskFileTeam, directory_path
from .forms import ProjectForm, TaskFileForm, ProjectStatusForm, TaskOfferForm, TaskOfferResponseForm, TaskPermissionForm, DeliveryForm, TaskDeliveryResponseForm, TeamForm, TeamAddForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def projects(request):
    projects = Project.objects.all()
    project_categories = ProjectCategory.objects.all()
    common_tags_all = Project.tags.most_common()[:6]
    common_tags = {}

    return render(request,
        'projects/projects.html',
        {
            'projects': projects,
            'project_categories': project_categories,
            'common_tags': common_tags,
            'common_tags_all': common_tags_all,
        }
    )

@login_required
def new_project(request):
    from django.contrib.sites.shortcuts import get_current_site
    current_site = get_current_site(request)
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user.profile
            project.category =  get_object_or_404(ProjectCategory, id=request.POST.get('category_id'))
            project.save()
            # Without this next line the tags won't be saved 
            form.save_m2m()

            people = Profile.objects.filter(categories__id=project.category.id)
            from django.core import mail
            for person in people:
                if person.user.email:
                    try:
                        with mail.get_connection() as connection:
                            mail.EmailMessage(
                                "New Project: " + project.title , "A new project you might be interested in was created and can be viwed at " + current_site.domain + '/projects/' + str(project.id), "Agreelancer", [person.user.email],
                                connection=connection,
                            ).send()
                    except Exception as e:
                        from django.contrib import messages
                        messages.success(request, 'Sending of email to ' + person.user.email + " failed: " + str(e))

            task_title = request.POST.getlist('task_title')
            task_description = request.POST.getlist('task_description')
            task_budget = request.POST.getlist('task_budget')
            for i in range(0, len(task_title)):
                Task.objects.create(
                    title = task_title[i],
                    description = task_description[i],
                    budget = task_budget[i],
                    project = project,
                )
            return redirect('project_view', project_id=project.id)
    else:
        form = ProjectForm()
    return render(request, 'projects/new_project.html', {'form': form})


def project_view(request, project_id):
    project = Project.objects.get(pk=project_id)
    tasks = project.tasks.all()
    total_budget = 0 # Initializes the total budget to 0

    for item in tasks:
        total_budget += item.budget

    if request.user == project.user.user:

        if request.method == 'POST' and 'offer_response' in request.POST:
            instance = get_object_or_404(TaskOffer, id=request.POST.get('taskofferid'))
            offer_response_form = TaskOfferResponseForm(request.POST, instance=instance)
            if offer_response_form.is_valid():
                offer_response = offer_response_form.save(commit=False)

                if offer_response.status == 'a':
                    offer_response.task.read.add(offer_response.offerer)
                    offer_response.task.write.add(offer_response.offerer)
                    project = offer_response.task.project
                    project.participants.add(offer_response.offerer)


                offer_response.save()
        offer_response_form = TaskOfferResponseForm()

        if request.method == 'POST' and 'status_change' in request.POST:
            status_form = ProjectStatusForm(request.POST)
            if status_form.is_valid():
                project_status = status_form.save(commit=False)
                project.status = project_status.status
                project.save()
        status_form = ProjectStatusForm(initial={'status': project.status})

        return render(request, 'projects/project_view.html', {
        'project': project,
        'tasks': tasks,
        'status_form': status_form,
        'total_budget': total_budget,
        'offer_response_form': offer_response_form,
        })


    else:
        if request.method == 'POST' and 'offer_submit' in request.POST:
            task_offer_form = TaskOfferForm(request.POST)
            if task_offer_form.is_valid():
                task_offer = task_offer_form.save(commit=False)
                task_offer.task =  Task.objects.get(pk=request.POST.get('taskvalue'))
                task_offer.offerer = request.user.profile
                task_offer.save()
        task_offer_form = TaskOfferForm()

        return render(request, 'projects/project_view.html', {
        'project': project,
        'tasks': tasks,
        'task_offer_form': task_offer_form,
        'total_budget': total_budget,
        })


def isProjectOwner(user, project):
    return user == project.user.user


@login_required
def upload_file_to_task(request, project_id, task_id):
    project = Project.objects.get(pk=project_id)
    task = Task.objects.get(pk=task_id)
    user_permissions = get_user_task_permissions(request.user, task)
    accepted_task_offer = task.accepted_task_offer()

    if user_permissions['modify'] or user_permissions['write'] or user_permissions['upload'] or isProjectOwner(request.user, project):
        if request.method == 'POST':
            task_file_form = TaskFileForm(request.POST, request.FILES)
            if task_file_form.is_valid():
                task_file = task_file_form.save(commit=False)
                task_file.task = task
                existing_file = task.files.filter(file=directory_path(task_file, task_file.file.file)).first()
                access = user_permissions['modify'] or user_permissions['owner']
                access_to_file = False # Initialize access_to_file to false
                for team in request.user.profile.teams.all():
                    file_modify_access  = TaskFileTeam.objects.filter(team=team, file=existing_file, modify=True).exists()
                    print(file_modify_access)
                    access = access or file_modify_access
                access = access or user_permissions['modify']
                if (access):
                    if existing_file:
                        existing_file.delete()
                    task_file.save()

                    if request.user.profile != project.user and request.user.profile != accepted_task_offer.offerer:
                        teams = request.user.profile.teams.filter(task__id=task.id)
                        for team in teams:
                            tft = TaskFileTeam()
                            tft.team = team
                            tft.file = task_file
                            tft.read = True
                            tft.save()
                else:
                    from django.contrib import messages
                    messages.warning(request, "You do not have access to modify this file")

                return redirect('task_view', project_id=project_id, task_id=task_id)

        task_file_form = TaskFileForm()
        return render(
            request,
            'projects/upload_file_to_task.html',
            {
                'project': project,
                'task': task,
                'task_file_form': task_file_form,
            }
        )
    return redirect('/user/login') # Redirects to /user/login

def get_user_task_permissions(user, task):

    if user == task.project.user.user:
        return {
            'write': True,
            'read': True,
            'modify': True,
            'owner': True,
            'upload': True,
        }
    if task.accepted_task_offer() and task.accepted_task_offer().offerer == user.profile:
        return {
            'write': True,
            'read': True,
            'modify': True,
            'owner': False,
            'upload': True,
        }
    user_permissions = {
        'write': False,
        'read': False,
        'modify': False,
        'owner': False,
        'view_task': False,
        'upload': False,
    }
    user_permissions['read'] = user_permissions['read'] or user.profile.task_participants_read.filter(id=task.id).exists()

    # Team members can view its teams tasks
    user_permissions['upload'] = user_permissions['upload'] or user.profile.teams.filter(task__id=task.id, write=True).exists()
    user_permissions['view_task'] = user_permissions['view_task'] or user.profile.teams.filter(task__id=task.id).exists()

    user_permissions['write'] = user_permissions['write'] or user.profile.task_participants_write.filter(id=task.id).exists()
    user_permissions['modify'] = user_permissions['modify'] or user.profile.task_participants_modify.filter(id=task.id).exists()

    return user_permissions

@login_required
def task_view(request, project_id, task_id):
    user = request.user
    project = Project.objects.get(pk=project_id)
    task = Task.objects.get(pk=task_id)
    accepted_task_offer = task.accepted_task_offer()

    user_permissions = get_user_task_permissions(request.user, task)
    if not user_permissions['read'] and not user_permissions['write'] and not user_permissions['modify'] and not user_permissions['owner'] and not user_permissions['view_task']:
        return redirect('/user/login')


    if request.method == 'POST' and 'delivery' in request.POST:
        if accepted_task_offer and accepted_task_offer.offerer == user.profile:
            deliver_form = DeliveryForm(request.POST, request.FILES)
            if deliver_form.is_valid():
                delivery = deliver_form.save(commit=False)
                delivery.task = task
                delivery.delivery_user = user.profile
                delivery.save()
                task.status = "pa"
                task.save()

    if request.method == 'POST' and 'delivery-response' in request.POST:
        instance = get_object_or_404(Delivery, id=request.POST.get('delivery-id'))
        deliver_response_form = TaskDeliveryResponseForm(request.POST, instance=instance)
        if deliver_response_form.is_valid():
            delivery = deliver_response_form.save()
            from django.utils import timezone
            delivery.responding_time = timezone.now()
            delivery.responding_user = user.profile
            delivery.save()

            if delivery.status == 'a':
                task.status = "pp"
                task.save()
            elif delivery.status == 'd':
                task.status = "dd"
                task.save()

    if request.method == 'POST' and 'team' in request.POST:
        if accepted_task_offer and accepted_task_offer.offerer == user.profile:
            team_form = TeamForm(request.POST)
            if (team_form.is_valid()):
                team = team_form.save(False)
                team.task = task
                team.save()


    if request.method == 'POST' and 'team-add' in request.POST:
        if accepted_task_offer and accepted_task_offer.offerer == user.profile:
            instance = get_object_or_404(Team, id=request.POST.get('team-id'))
            team_add_form = TeamAddForm(request.POST, instance=instance)
            if team_add_form.is_valid():
                team = team_add_form.save(False)
                team.members.add(*team_add_form.cleaned_data['members'])
                team.save()

    if request.method == 'POST' and 'permissions' in request.POST:
        if accepted_task_offer and accepted_task_offer.offerer == user.profile:
            for t in task.teams.all():
                for f in task.files.all():
                    try:
                        tft_string = 'permission-perobj-' + str(f.id) + '-' + str(t.id)
                        tft_id=request.POST.get(tft_string)
                        instance = TaskFileTeam.objects.get(id=tft_id)
                    except Exception as e:
                        instance = TaskFileTeam(
                            file = f,
                            team = t,
                        )

                    instance.read = request.POST.get('permission-read-' + str(f.id) + '-' + str(t.id))  or False
                    instance.write = request.POST.get('permission-write-' + str(f.id) + '-' + str(t.id)) or False
                    instance.modify = request.POST.get('permission-modify-' + str(f.id) + '-' + str(t.id))  or False
                    instance.save()
                t.write = request.POST.get('permission-upload-' + str(t.id)) or False
                t.save()


    deliver_form = DeliveryForm()
    deliver_response_form = TaskDeliveryResponseForm()
    team_form = TeamForm()
    team_add_form = TeamAddForm()


    if user_permissions['read'] or user_permissions['write'] or user_permissions['modify'] or user_permissions['owner'] or user_permissions['view_task']:
        deliveries = task.delivery.all()
        team_files = []
        teams = user.profile.teams.filter(task__id=task.id).all()
        per = {}
        for f in task.files.all():
            per[f.name()] = {}
            for p in f.teams.all():
                per[f.name()][p.team.name] = p
                if p.read:
                    team_files.append(p)
        return render(request, 'projects/task_view.html', {
                'task': task,
                'project': project,
                'user_permissions': user_permissions,
                'deliver_form': deliver_form,
                'deliveries': deliveries,
                'deliver_response_form': deliver_response_form,
                'team_form': team_form,
                'team_add_form': team_add_form,
                'team_files': team_files,
                'per': per
                })

    return redirect('/user/login')

@login_required
def task_permissions(request, project_id, task_id):
    user = request.user
    task = Task.objects.get(pk=task_id)
    project = Project.objects.get(pk=project_id)
    accepted_task_offer = task.accepted_task_offer()
    if project.user == request.user.profile or user == accepted_task_offer.offerer.user:
        task = Task.objects.get(pk=task_id)
        if int(project_id) == task.project.id:
            if request.method == 'POST':
                task_permission_form = TaskPermissionForm(request.POST)
                if task_permission_form.is_valid():
                    try:
                        username = task_permission_form.cleaned_data['user']
                        user = User.objects.get(username=username)
                        permission_type =task_permission_form.cleaned_data['permission']
                        if permission_type == 'Read':
                            task.read.add(user.profile)
                        elif permission_type == 'Write':
                            task.write.add(user.profile)
                        elif permission_type == 'Modify':
                            task.modify.add(user.profile)
                    except (Exception):
                        print("user not found")
                    return redirect('task_view', project_id=project_id, task_id=task_id)

            task_permission_form = TaskPermissionForm()
            return render(
                request,
                'projects/task_permissions.html',
                {
                    'project': project,
                    'task': task,
                    'form': task_permission_form,
                }
            )
    return redirect('task_view', project_id=project_id, task_id=task_id)


@login_required
def delete_file(request, file_id):
    f = TaskFile.objects.get(pk=file_id)
    f.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
