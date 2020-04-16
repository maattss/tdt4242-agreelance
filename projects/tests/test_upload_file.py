from django.test import TestCase
from projects.views import project_view
from projects.views.task_view import upload_file_to_task
from projects.models import ProjectCategory, Project, Task, TaskOffer, Delivery, TaskFile
from user.models import Profile
from faker import Faker
from django.contrib.auth.models import User
from django.test import RequestFactory
from django.http import Http404
from unittest import skip

import os

# Accept offer output coverage tests
class TestUploadFile(TestCase):
    def setUp(self):
        self.fake = Faker() # Generate fake data using a faker generator
        
        self.factory = RequestFactory()
        self.project_category = ProjectCategory.objects.create(pk=1)

        # Firs user is project owner and second user creates offer
        self.first_user = User.objects.create_user(
            pk=1,
            username=self.fake.user_name(),
            password=self.fake.password())
        self.second_user = User.objects.create_user(
            pk=2,
            username=self.fake.user_name(),
            password=self.fake.password())
        
        self.first_profile = Profile.objects.get(user=self.first_user)
        self.second_profile = Profile.objects.get(user=self.second_user)

        self.project = Project.objects.create(
            pk=1,
            user=self.first_profile,
            category=self.project_category)

        self.first_task = Task.objects.create(project=self.project)

        self.first_task_offer = TaskOffer(
            task=self.first_task,
            offerer=self.second_profile,
            status = 'a')
        
        self.first_task_offer.save()

        self.delivery = Delivery.objects.create(
            task=self.first_task,
            delivery_user=self.second_profile
        )

    def test_upload_file(self):
        f = open("projects/tests/demofile.txt", "r")
        request = self.factory.post('/projects/' + str(self.project.id) + '/tasks/' + str(self.first_task.id) + '/upload/', {
            'file': f
        })
        request.user = self.first_user
        upload_file_to_task(request, self.project.id, self.first_task.id)
        db_file = None
        try:
            db_delivery = TaskFile.objects.get(task = self.first_task)
            db_file = db_delivery.file
        except:
            pass
        self.assertEquals(db_file, "static/uploads/tasks/" + str(self.first_task.id) + "/demofile.txt")
    
    