from projects.models import Project, Task, Delivery, Team, TaskFileTeam, directory_path
from projects.forms import TaskFileForm, TaskPermissionForm, DeliveryForm, TaskDeliveryResponseForm, TeamForm, TeamAddForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from user.review_functions import average_rating
from django.core.exceptions import ObjectDoesNotExist

# Constants
USER_LOGIN = "/user/login"

@login_required
def task_view(request, project_id, task_id):
    user = request.user
    project = Project.objects.get(pk=project_id)
    task = Task.objects.get(pk=task_id)
    accepted_task_offer = task.accepted_task_offer()

    user_permissions = get_user_task_permissions(request.user, task)
    if not user_permissions['read'] and not user_permissions['write'] and not user_permissions['modify'] and not user_permissions['owner'] and not user_permissions['view_task']:
        return redirect(USER_LOGIN)

    if request.method == 'POST' and 'delivery' in request.POST and accepted_task_offer and accepted_task_offer and accepted_task_offer.offerer == user.profile:
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
            if delivery.status == 'a': # Accepted
                task.status = "pp"
                task.save()
            elif delivery.status == 'd': # Declined
                task.status = "dd"
                task.save()

    if request.method == 'POST' and 'team' in request.POST and accepted_task_offer and accepted_task_offer.offerer == user.profile:
        team_form = TeamForm(request.POST)
        if (team_form.is_valid()):
            team = team_form.save(False)
            team.task = task
            team.save()

    if request.method == 'POST' and 'team-add' in request.POST and accepted_task_offer and accepted_task_offer.offerer == user.profile:
        instance = get_object_or_404(Team, id=request.POST.get('team-id'))
        team_add_form = TeamAddForm(request.POST, instance=instance)
        if team_add_form.is_valid():
            team = team_add_form.save(False)
            team.members.add(*team_add_form.cleaned_data['members'])
            team.save()

    if request.method == 'POST' and 'permissions' in request.POST and \
        accepted_task_offer and accepted_task_offer.offerer == user.profile:
        for t in task.teams.all():
            for f in task.files.all():
                permission_helper(request, current_team = t, current_file = f)
            t.write = request.POST.get('permission-upload-' + str(t.id)) or False
            t.save()

    deliver_form = DeliveryForm()
    deliver_response_form = TaskDeliveryResponseForm()
    team_form = TeamForm()
    team_add_form = TeamAddForm()

    if user_permissions['read'] or user_permissions['write'] or user_permissions['modify'] or user_permissions['owner'] or user_permissions['view_task']:
        deliveries = task.delivery.all()
        team_files = []
        avg_rating = None
        try:
            avg_rating = average_rating(accepted_task_offer.offerer.user_id)
        except:
            pass
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
                'per': per,
                'avg_rating': avg_rating
                })
    return redirect(USER_LOGIN)

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

def handle_valid_file_form(task_file_form, task, request, user_permissions, project):
    task_file = task_file_form.save(commit=False)
    task_file.task = task
    existing_file = task.files.filter(file=directory_path(task_file, task_file.file.file)).first()
    access = user_permissions['modify'] or user_permissions['owner']
    accepted_task_offer = task.accepted_task_offer()
    for team in request.user.profile.teams.all():
        file_modify_access  = TaskFileTeam.objects.filter(team=team, file=existing_file, modify=True).exists()
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

@login_required
def upload_file_to_task(request, project_id, task_id):
    project = Project.objects.get(pk=project_id)
    task = Task.objects.get(pk=task_id)
    user_permissions = get_user_task_permissions(request.user, task)

    if user_permissions['modify'] or user_permissions['write'] or user_permissions['upload'] or is_project_owner(request.user, project):
        if request.method == 'POST':
            task_file_form = TaskFileForm(request.POST, request.FILES)
            if task_file_form.is_valid():
                handle_valid_file_form(task_file_form, task, request, user_permissions, project)
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
    return redirect(USER_LOGIN) # Redirects to /user/login

# Helpers
def isProjectOwner(user, project):
    return user == project.user.user

def permission_helper(request, current_team, current_file):
    try:
        task_file_team_string = 'permission-perobj-' + str(current_file.id) + '-' + str(current_team.id)
        task_file_team_id = request.POST.get(task_file_team_string)
        instance = TaskFileTeam.objects.get(id=task_file_team_id)
    except ObjectDoesNotExist:
        # Create new instance if it does not exist
        instance = TaskFileTeam(file = current_file, team = current_team)
    instance.read = request.POST.get('permission-read-' 
        + str(current_file.id) + '-' + str(current_team.id)) or False
    instance.write = request.POST.get('permission-write-' 
        + str(current_file.id) + '-' + str(current_team.id)) or False
    instance.modify = request.POST.get('permission-modify-' 
        + str(current_file.id) + '-' + str(current_team.id))  or False
    instance.save()

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