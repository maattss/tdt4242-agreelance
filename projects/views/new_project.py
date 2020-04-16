from user.models import Profile
from projects.models import Task, ProjectCategory
from projects.forms import ProjectForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def new_project(request):
    from django.contrib.sites.shortcuts import get_current_site
    current_site = get_current_site(request)
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user.profile
            category = get_object_or_404(ProjectCategory, id=request.POST.get('category_id'))
            project.category = category
            tags = request.POST.get('tags').split(",")
            for tag in tags:
               category.tags.add(tag.replace(" ", ""))
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
