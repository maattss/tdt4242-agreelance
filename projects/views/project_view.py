from projects.models import Project, Task, TaskOffer, ProjectCategory
from projects.forms import ProjectStatusForm, TaskOfferForm, TaskOfferResponseForm
from django.shortcuts import render, get_object_or_404
from user.review_functions import average_rating

# Constants
PROJECTS_TEMPLATE = "projects/projects.html"

def projects_all(request):
    projects = Project.objects.all()
    project_categories = ProjectCategory.objects.all()
    current_category = project_categories[0]
    common_tags = current_category.tags.most_common()[:6]

    return render(request,
        PROJECTS_TEMPLATE,
        {
            'projects': projects,
            'project_categories': project_categories,
            'current_project_category': current_category,
            'common_tags': common_tags,
        }
    )

def projects(request, category_id):
    all_projects = Project.objects.all()
    relevant_projects = []

    for project in all_projects: # Find relevant project for this category
        if str(project.category.id) == str(category_id):
            relevant_projects.append(project)
    
    project_categories = ProjectCategory.objects.all()
    current_category = project_categories[int(category_id)-1]
    common_tags = current_category.tags.most_common()[:6]

    return render(request,
        PROJECTS_TEMPLATE,
        {
            'projects': relevant_projects,
            'project_categories': project_categories,
            'current_project_category': current_category,
            'common_tags': common_tags,
        }
    )

def projects_tags(request, category_id, tag_name):
    all_projects = Project.objects.all()
    relevant_projects = filter_tags(all_projects, category_id, tag_name)

    project_categories = ProjectCategory.objects.all()
    current_category = project_categories[int(category_id)-1]
    common_tags = current_category.tags.most_common()[:6]

    return render(request,
        PROJECTS_TEMPLATE,
        {
            'projects': relevant_projects,
            'project_categories': project_categories,
            'current_project_category': current_category,
            'common_tags': common_tags,
            'searched_tag': tag_name,
        }
    )


def filter_tags(all_projects, category_id, tag_name):
    relevant_projects = []
    for project in all_projects: # Filter project that does is not in chosen category
        if str(project.category.id) == str(category_id):
            tag_included = False
            for tag in project.tags.all(): # Filter projects that does not include relevant tag
                if str(tag_name) == str(tag):
                    tag_included = True
                    break
            if tag_included:
                relevant_projects.append(project)
    return relevant_projects

def project_view(request, project_id):
    project = Project.objects.get(pk=project_id)
    tasks = project.tasks.all()
    total_budget = 0 # Initializes the total budget to 0
    
    publisher = project.user.user.username
    publisher_id = project.user.user.id
    publisher_rating = average_rating(publisher_id)
    if (publisher_rating == 0):
        publisher_rating = "No reviews"

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
        'publisher': publisher,
        'publisher_id': publisher_id,
        'publisher_rating': publisher_rating
        })


    else:
        if request.method == 'POST' and 'offer_submit' in request.POST:
            task_offer_form = TaskOfferForm(request.POST)
            if task_offer_form.is_valid():
                task_offer = task_offer_form.save(commit=False)
                task_offer.task = Task.objects.get(pk=request.POST.get('taskvalue'))
                task_offer.offerer = request.user.profile
                task_offer.save()
        task_offer_form = TaskOfferForm()

        return render(request, 'projects/project_view.html', {
        'project': project,
        'tasks': tasks,
        'task_offer_form': task_offer_form,
        'total_budget': total_budget,
        'publisher': publisher,
        'publisher_id': publisher_id,
        'publisher_rating': publisher_rating
        })