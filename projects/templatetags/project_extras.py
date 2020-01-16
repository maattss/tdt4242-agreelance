from django import template
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from ..models import TaskOffer

register = template.Library()

#### Unnecessary
@register.filter
def get_owner(value):
    user = User.objects.get(profile = value)
    return user.username

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key) if dictionary else dictionary

@register.filter
def read(per):
    return per.read if per else 0

@register.filter
def write(per):
    return per.write if per else 0

@register.filter
def modify(per):
    return per.modify if per else 0

@register.filter
def id(per):
    return per.id if per else None

@register.simple_tag
def define(val=None):
  return val


@register.filter
def check_taskoffers(task, user):
    taskoffers = task.taskoffer_set.filter(offerer=user.profile)
    useroffers = []

    for item in taskoffers:
        useroffers.append(item)

    return useroffers


@register.filter
def get_all_taskoffers(value):
    taskoffers = value.taskoffer_set.all()
    return taskoffers

@register.filter
def get_accepted_task_offer(task):
    task_offer = None
    try:
        task_offer = task.taskoffer_set.get(status='a')
    except TaskOffer.DoesNotExist:
        pass

    return task_offer

@register.filter
def get_project_participants_string(project):

    participants_string = ', '.join(get_project_participants(project))

    return participants_string

def get_project_participants(project):
    query = project.participants.all()
    participants = set()
    for participant in query:
        participants.add(participant.user.username)

    return participants
