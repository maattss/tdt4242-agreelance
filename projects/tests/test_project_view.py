from django.test import TestCase
from projects.views import project_view, get_user_task_permissions, new_project, projects_tags, filter_tags
from projects.models import ProjectCategory, Project, Task, TaskOffer
from user.models import Profile
from faker import Faker
from factory.fuzzy import FuzzyText, FuzzyInteger
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from projects.forms import TaskOfferForm
from taggit.managers import TaggableManager
from unittest import skip
from django.http import Http404

# Full statement coverage test of the project_view() function
class TestProjectView(TestCase):
    def setUp(self):
        fake = Faker() # Generate fake data using a faker generator

        self.factory = RequestFactory()
        self.project_category = ProjectCategory.objects.create(pk=1)

        self.first_user = User.objects.create_user(
            pk=1,
            username=fake.user_name(),
            password=fake.password())
        self.second_user = User.objects.create_user(
            pk=2,
            username=fake.user_name(),
            password=fake.password())
        
        self.profile = Profile.objects.get(user=self.first_user)

        self.project = Project.objects.create(
            pk=1,
            user=self.profile,
            category=self.project_category)

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