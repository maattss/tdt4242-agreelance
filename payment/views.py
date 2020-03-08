
from django.shortcuts import render, redirect

from .models import Payment
from projects.models import Project, Task, TaskOffer
from projects.templatetags.project_extras import get_accepted_task_offer
from .forms import PaymentForm
from django.contrib.auth.decorators import login_required


@login_required
def payment(request, project_id, task_id):
    task = Task.objects.get(pk=task_id)
    sender = Project.objects.get(pk=project_id).user
    receiver = get_accepted_task_offer(task).offerer

    if request.method == 'POST':
        payment = Payment(payer=sender, receiver=receiver, task=task)
        payment.save()
        task.status = Task.PAYMENT_SENT # Set task status to payment sent
        task.save()
        
        from django.core import mail
        from django.contrib.sites.shortcuts import get_current_site
        current_site = get_current_site(request)
        
        # Send mail to both users for leaving review for each other when payment is completed
        if receiver.user.email:
            try:
                with mail.get_connection() as connection:
                    mail.EmailMessage(
                        "Leave a review",
                        "Congratulation on finishing a task!\nLeave a review for how it was working for " + sender.user.username + " here:\n" + "https://" + current_site.domain + "/user/set_review/" + str(sender.user_id), 
                        "Agreelancer", 
                        [receiver.user.email],
                        connection=connection,
                    ).send()
            except Exception as e:
                from django.contrib import messages
                messages.success(request, 'Sending of email to ' + receiver.user.email + " failed: " + str(e))
        if sender.user.email:
            try:
                with mail.get_connection() as connection:
                    mail.EmailMessage(
                        "Leave a review",
                        "Congratulation, your task has been finished!\nLeave a review for how it was working with " + receiver.user.username + " here:\n" + "https://" + current_site.domain + "/user/set_review/" + str(receiver.user_id), 
                        "Agreelancer", 
                        [sender.user.email],
                        connection=connection,
                    ).send()
            except Exception as e:
                from django.contrib import messages
                messages.success(request, 'Sending of email to ' + sender.user.email + " failed: " + str(e))

        return redirect('receipt', project_id=project_id, task_id=task_id)

    form = PaymentForm()

    return render(request,
                'payment/payment.html', {
                'form': form,
                })

@login_required
def receipt(request, project_id, task_id):
    project = Project.objects.get(pk=project_id)
    task = Task.objects.get(pk=task_id)
    taskoffer = get_accepted_task_offer(task)

    return render(request,
                'payment/receipt.html', {
                'project': project,
                'task': task,
                'taskoffer': taskoffer,
                })
