from django.test import TestCase, Client
from projects.views import project_view, get_user_task_permissions
from projects.models import ProjectCategory, Project, Task, TaskOffer
from user.models import Profile
from faker import Faker
from factory.fuzzy import FuzzyText, FuzzyInteger
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from .forms import TaskOfferForm

# Full statement coverage test of the get_user_task_permission() function
class TestGetUserTaskPermissions(TestCase):
    def setUp(self):
        fake = Faker() # Generate fake data using a faker generator

        self.project_category = ProjectCategory.objects.create(pk=1)
        
        self.first_user = User.objects.create_user(
            pk=1,
            username=fake.user_name(),
            password=fake.password())
        self.second_user = User.objects.create_user(
            pk=2,
            username=fake.user_name(),
            password=fake.password())
        
        self.first_profile = Profile.objects.get(user=self.first_user)
        self.second_profile = Profile.objects.get(user=self.second_user)
        
        self.project = Project.objects.create(
            pk=1,
            user=self.first_profile,
            category=self.project_category)
        
        self.first_task = Task.objects.create(project=self.project)
        self.second_task = Task.objects.create(project=self.project)

        self.task_offer = TaskOffer.objects.create(
            task=self.second_task,
            offerer=self.second_profile,
            status='a')

    # Test owner permissions - All permissions
    def test_user_owner(self):
        self.assertEquals(get_user_task_permissions(self.first_user, self.first_task),
            {
                'write': True,
                'read': True,
                'modify': True,
                'owner': True,
                'upload': True,
            })

    # Test accepted offer permissions - Some permissions
    def test_user_accepted(self):
        self.assertEquals(get_user_task_permissions(self.second_user, self.second_task),
            {
                'write': True,
                'read': True,
                'modify': True,
                'owner': False,
                'upload': True,
            })

    # Test regular user permissions - No permissions
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

# Boundary value test for giving project offers
class TestGiveProjectOffers(TestCase):
    def setUp(self):
         # Boundary values for number of characters in fields
        self.max_title = FuzzyText(length=200)
        self.max_description = FuzzyText(length=500)
        self.min = FuzzyText(length=1)
        
        # Choosing max and min as above and below zero. 
        # Price input does not specify any boundaries. 
        self.max_price = FuzzyInteger(0, 9999)
        self.min_price = FuzzyInteger(-9999, -1)
    
    def test_max_values(self):
        data = {
            'title': self.max_title.fuzz(),
            'description': self.max_description.fuzz(),
            'price': self.max_price.fuzz()
        }
        form = TaskOfferForm(data)
        self.assertTrue(form.is_valid())

    def test_min_values(self):
        data = {
            'title': self.min.fuzz(),
            'description': self.min.fuzz(),
            'price': self.min_price.fuzz()
        }
        form = TaskOfferForm(data)
        self.assertTrue(form.is_valid())


'''
class TestAcceptingOffersBugs(TestCase):
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
            offerer=self.profile,
            status='p')
        self.task_offer.save()

    def test_bugs(self):
'''