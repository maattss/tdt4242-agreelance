from django import template
from projects.models import Project, Task, TaskOffer

register = template.Library()

@register.filter
def check_nr_pending_offers(project):
    pending_offers = 0
    tasks = project.tasks.all()
    for task in tasks:
        taskoffers = task.taskoffer_set.all()
        for taskoffer in taskoffers:
            if taskoffer.status == TaskOffer.PENDING:
                pending_offers+=1
    return pending_offers


@register.filter
def check_nr_user_offers(project, user):
    offers = {}
    pending_offers = 0
    declined_offers = 0
    accepted_offers = 0
    tasks = project.tasks.all()
    for task in tasks:
        taskoffers = task.taskoffer_set.filter(offerer=user.profile)
        for taskoffer in taskoffers:
            if taskoffer.status == TaskOffer.PENDING:
                pending_offers+=1
            elif taskoffer.status == TaskOffer.ACCEPTED:
                accepted_offers+=1
            elif taskoffer.status == TaskOffer.DECLINED:
                declined_offers+=1

    offers['declined'] = declined_offers
    offers['pending'] = pending_offers
    offers['accepted'] = accepted_offers
    return offers

@register.filter
def task_status(task):
    if task.status == Task.PENDING_ACCEPTANCE:
        return "You have deliveries waiting for acceptance"
    elif task.status == Task.PENDING_PAYMENT:
        return "You have deliveries waiting for payment"
    elif task.status == Task.PAYMENT_SENT:
        return "You have sent payment"
    return "You are awaiting delivery"


@register.filter
def get_task_statuses(project):
    task_statuses = {}

    awaiting_delivery = 0
    pending_acceptance = 0
    pending_payment = 0
    payment_sent = 0
    declined_delivery = 0

    tasks = project.tasks.all()
    for task in tasks:
        if task.status == Task.AWAITING_DELIVERY:
            awaiting_delivery+=1
        elif task.status == Task.PENDING_ACCEPTANCE:
            pending_acceptance+=1
        elif task.status == Task.PENDING_PAYMENT:
            pending_payment+=1
        elif task.status == Task.PAYMENT_SENT:
            payment_sent+=1
        elif task.status == Task.DECLINED_DELIVERY:
            declined_delivery+=1

    task_statuses['awaiting_delivery'] = awaiting_delivery
    task_statuses['pending_acceptance'] = pending_acceptance
    task_statuses['pending_payment'] = pending_payment
    task_statuses['payment_sent'] = payment_sent
    task_statuses['declined_delivery'] = declined_delivery

    return task_statuses

@register.filter
def all_tasks(project):
    return project.tasks.all()

@register.filter
def offers(task):
    task_offers = task.taskoffer_set.all()
    msg = "No offers"
    if len(task_offers) > 0:
        x = 0
        msg = "You have "
        for t in task_offers:
            x+=1
            if t.status == 'a':
                return "You have accepted an offer for this task"
        msg += str(x) + " pending offers"
    return msg

@register.filter
def get_user_task_statuses(project, user):
    task_statuses = {}

    awaiting_delivery = 0
    pending_acceptance = 0
    pending_payment = 0
    payment_sent = 0
    declined_delivery = 0

    tasks = project.tasks.all()

    for task in tasks:
        try:
            task_offer = task.taskoffer_set.get(status='a')
            if task_offer.offerer == user.profile:
                if task.status == Task.AWAITING_DELIVERY:
                    awaiting_delivery+=1
                elif task.status == Task.PENDING_ACCEPTANCE:
                    pending_acceptance+=1
                elif task.status == Task.PENDING_PAYMENT:
                    pending_payment+=1
                elif task.status == Task.PAYMENT_SENT:
                    payment_sent+=1
                elif task.status == Task.DECLINED_DELIVERY:
                    declined_delivery+=1

        except TaskOffer.DoesNotExist:
            pass


    task_statuses['awaiting_delivery'] = awaiting_delivery
    task_statuses['pending_acceptance'] = pending_acceptance
    task_statuses['pending_payment'] = pending_payment
    task_statuses['payment_sent'] = payment_sent
    task_statuses['declined_delivery'] = declined_delivery

    return task_statuses
