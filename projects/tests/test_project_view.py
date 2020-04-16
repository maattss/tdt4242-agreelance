from django.test import TestCase, RequestFactory
from projects.views import project_view
from projects.models import ProjectCategory, Project, Task, TaskOffer
from user.models import Profile
from faker import Faker
from django.contrib.auth.models import User

PROJECTS_ALL = "/projects_all/"

# Full statement coverage test of the project_view() function
class TestProjectView(TestCase):
    def setUp(self):
        self.fake = Faker() # Generate fake data using a faker generator

        self.factory = RequestFactory()
        self.project_category = ProjectCategory.objects.create(pk=1)

        self.first_user = User.objects.create_user(
            pk=1,
            username=self.fake.user_name(),
            password=self.fake.password())
        self.second_user = User.objects.create_user(
            pk=2,
            username=self.fake.user_name(),
            password=self.fake.password())
        
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
        request = self.factory.post(PROJECTS_ALL, {
            'offer_response': '',
            'taskofferid': 1,
            'status': 'a',
            'feedback': self.fake.sentence(nb_words=10)
        })
        request.user = self.first_user
        response = project_view.project_view(request, 1)
        self.assertEqual(response.status_code, 200)

    def test_status_change(self):
        request = self.factory.post(PROJECTS_ALL, {
            'status_change': '',
            'status': self.project.status
        })
        request.user = self.first_user
        response = project_view.project_view(request, 1)
        self.assertEqual(response.status_code, 200)

    def test_offer_submit(self):
        request = self.factory.post(PROJECTS_ALL, {
            'offer_submit': '',
            'title': self.fake.sentence(nb_words=3),
            'description': self.fake.sentence(nb_words=5),
            'price': self.fake.random_int(min=10, max=100000, step=10),
            'taskvalue': 1
        })
        request.user = self.second_user
        response = project_view.project_view(request, 1)
        self.assertEqual(response.status_code, 200)