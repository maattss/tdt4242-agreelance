from django.db import models

from projects.models import Task
from user.models import Profile

class Payment(models.Model):
    payer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="payer")
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="receiver")
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return self.payer.user.username + " " + self.receiver.user.username + " " + str(self.task.budget)
