from django.test import TestCase, Client
from projects.views import project_view, get_user_task_permissions
from projects.models import ProjectCategory, Project, Task, TaskOffer
from user.models import Profile

from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase

class TestGetUserTaskPermissions(TestCase):
    def setUp(self):
        self.pCategory = ProjectCategory.objects.create(pk=1)
        
        self.first_user = User.objects.create_user(
            pk=1,
            username='User1',
            password='guAXb81#cAFV')
        self.second_user = User.objects.create_user(
            pk=2,
            username="User2",
            password="SwokT2!5LoSf")
        
        self.first_profile = Profile.objects.get(user=self.first_user)
        self.second_profile = Profile.objects.get(user=self.second_user)
        
        self.project = Project.objects.create(
            pk=1,
            user=self.first_profile,
            category=self.pCategory)
        
        self.first_task = Task.objects.create(project=self.project)
        self.second_task = Task.objects.create(project=self.project)

        self.task_offer = TaskOffer.objects.create(
            task=self.second_task,
            offerer=self.second_profile,
            status='a')

    def test_user_owner(self):
        self.assertEquals(get_user_task_permissions(self.first_user, self.first_task),
            {
                'write': True,
                'read': True,
                'modify': True,
                'owner': True,
                'upload': True,
            })

    def test_no_owner(self):
        self.assertEquals(get_user_task_permissions(self.second_user, self.first_task),
            {
                'write': False,
                'read': False,
                'modify': False,
                'owner': False,
                'view_task': False,
                'upload': False,
            })

    def test_user_accepted(self):
        
        self.assertEquals(get_user_task_permissions(self.second_user, self.second_task),
            {
                'write': True,
                'read': True,
                'modify': True,
                'owner': False,
                'upload': True,
            })

class Test_project_view(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.pCategory = ProjectCategory.objects.create(pk=1)

        self.first_user = User.objects.create_user(
            pk=1,
            username='User1',
            password='guAXb81#cAFV')
        self.second_user = User.objects.create_user(
            pk=2,
            username="User2",
            password="SwokT2!5LoSf")
        
        self.profile = Profile.objects.get(user=self.first_user)

        self.project = Project.objects.create(
            pk=1,
            user=self.profile,
            category=self.pCategory)

        self.task = Task.objects.create(project=self.project)

        self.task_offer = TaskOffer(
            task=self.task,
            offerer=self.profile)
        self.task_offer.save()

    def test_offer_response(self):
        request = self.factory.post('/projects_all/', {
            'offer_response': '',
            'taskofferid': 1,
            'status': 'a',
            'feedback': 'Feedback test'
        })
        request.user = self.first_user
        response = project_view(request, 1)
        self.assertEqual(response.status_code, 200)

    def test_status_change(self):
        request = self.factory.post('/projects_all/', {
            'status_change': '',
            'status': self.project.status
        })
        request.user = self.first_user
        response = project_view(request, 1)
        self.assertEqual(response.status_code, 200)

    def test_offer_submit(self):
        request = self.factory.post('/projects_all/', {
            'offer_submit': '',
            'title': 'Test title',
            'description': 'Test description',
            'price': 100,
            'taskvalue': 1
        })
        request.user = self.second_user
        response = project_view(request, 1)
        self.assertEqual(response.status_code, 200)
