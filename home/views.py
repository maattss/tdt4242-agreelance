from django.shortcuts import render, redirect
from pprint import pprint

from projects.models import Project

def home(request):
    if (request.user.is_authenticated):
        review_success = request.GET.get("review_success", "")
        user = request.user
        user_projects = Project.objects.filter(user = user.profile)
        customer_projects = list(Project.objects.filter(participants__id=user.id).order_by().distinct())
        for team in user.profile.teams.all():
            customer_projects.append(team.task.project)
        cd = {}
        for customer_project in customer_projects:
            cd[customer_project.id] = customer_project

        customer_projects = cd.values()
        given_offers_projects = Project.objects.filter(pk__in=get_given_offer_projects(user)).distinct()
        return render(
        request,
        'index.html',
        {
            'user_projects': user_projects,
            'customer_projects': customer_projects,
            'given_offers_projects': given_offers_projects,
            'review_success': review_success
        })
    else:
        return redirect('projects_all')

def get_given_offer_projects(user):
    project_ids = set()

    for taskoffer in user.profile.taskoffer_set.all():
        project_ids.add(taskoffer.task.project.id)

    return project_ids
