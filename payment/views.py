
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
