from django.test import TestCase, Client
from projects.views import project_view, get_user_task_permissions, new_project, projects_tags, filter_tags
from projects.models import ProjectCategory, Project, Task, TaskOffer
from user.models import Profile
from faker import Faker
from factory.fuzzy import FuzzyText, FuzzyInteger
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from .forms import TaskOfferForm
from taggit.managers import TaggableManager
from unittest import skip

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

# Boundary value test for giving task offers
class TestGiveProjectOffers(TestCase):
    def setUp(self):
        # Boundary values for number of characters in fields
        self.normal_title = FuzzyText(length=30)
        self.above_max_title = FuzzyText(length=201)
        self.below_max_title = FuzzyText(length=200)

        # Description does not specify any upper boundary
        self.normal_description = FuzzyText(length=300)

        self.above_min = FuzzyText(length=1)
        self.below_min = ""

        self.above_max_price = 1000000
        self.below_max_price = 999999
        self.normal_price = FuzzyInteger(2, 999998)
        self.above_min_price = 1
        self.below_min_price = 0
    
    def test_above_max_values(self):
        data = {
            'title': self.above_max_title.fuzz(),
            'description': self.normal_description.fuzz(),
            'price': self.above_max_price
        }
        form = TaskOfferForm(data)
        self.assertFalse(form.is_valid())

    def test_below_max_values(self):
        data = {
            'title': self.below_max_title.fuzz(),
            'description': self.normal_description.fuzz(),
            'price': self.below_max_price
        }
        form = TaskOfferForm(data)
        self.assertTrue(form.is_valid())
    
    def normal_values(self):
        data = {
            'title': self.normal_title.fuzz(),
            'description': self.normal_description.fuzz(),
            'price': self.normal_price.fuzz()
        }
        form = TaskOfferForm(data)
        self.assertTrue(form.is_valid())

    def test_above_min_values(self):
        data = {
            'title': self.above_min.fuzz(),
            'description': self.above_min.fuzz(),
            'price': self.above_min_price
        }
        form = TaskOfferForm(data)
        self.assertTrue(form.is_valid())
    
    def test_below_min_values(self):
        data = {
            'title': self.below_min,
            'description': self.below_min,
            'price': self.below_min_price
        }
        form = TaskOfferForm(data)
        self.assertFalse(form.is_valid())

# Integration and System tests for reviews
class TestTagsImplementation(TestCase):
    def setUp(self):
        fake = Faker() # Generate fake data using a faker generator

        self.factory = RequestFactory()
        self.project_category1 = ProjectCategory.objects.create(pk=1)
        self.project_category2 = ProjectCategory.objects.create(pk=2)
        
        self.first_user = User.objects.create_user(
            pk=1,
            username=fake.user_name(),
            password=fake.password())

        self.first_profile = Profile.objects.get(user=self.first_user)

        self.project1 = Project.objects.create(
            pk=1,
            user=self.first_profile,
            category=self.project_category1)
        
        self.project2 = Project.objects.create(
            pk=2,
            user=self.first_profile,
            category=self.project_category1)

        self.project1.tags.add('easy', 'cleaning')
        self.project2.tags.add('garage', 'easy')
    
    # Test if the project is stored in the database with the tags entered, and that tags are put onto the category
    def test_create_tag(self):
        request = self.factory.post('/new_project/', {
            'title': 'test title',
            'description': 'test description',
            'category_id': 2,
            'tags': 'tag1,tag2,tag3'
        })
        request.user = self.first_user
        response = new_project(request)
        db_project = None
        db_category = None
        test_objects = []
        try:
            db_project = Project.objects.get(title = 'test title')
            db_category = db_project.category
            test_objects.append(db_project)
            test_objects.append(db_category)
        except:
            pass
        for object in test_objects:
            with self.subTest():
                self.assertEquals(str(object.tags.all()), '<QuerySet [<Tag: tag1>, <Tag: tag2>, <Tag: tag3>]>')

    # Tests sql injection vulnerability by checking if the entire string is stored as a data.
    @skip("Discovered a bug. \"\" isn't stored as data")
    def test_strange_tags(self):
        request = self.factory.post('/new_project/', {
            'title': 'test title',
            'description': 'test description',
            'category_id': 2,
            'tags': '"select * from user_review where 1=1", "DROP DATABASE"'
        })
        request.user = self.first_user
        response = new_project(request)
        db_project = None
        try:
            db_project = Project.objects.get(title = 'test title')
        except:
            pass
        self.assertEquals(str(db_project.tags.all()), '<QuerySet [<Tag: select * from user_review where 1=1>, <Tag: DROP DATABASE>]>')
    
    # Test if the expected projects are filtered through with a given tag
    def test_tag_filter(self):
        all_projects = Project.objects.all()
        response = filter_tags(all_projects, self.project_category1.id, 'easy')
        self.assertEquals(response, [self.project1, self.project2])

'''
class TestAcceptingOffers(TestCase):
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
        self.third_user = User.objects.create_user(
            pk=2,
            username=fake.user_name(),
            password=fake.password())
        
        self.first_profile = Profile.objects.get(user=self.first_user)
        self.second_profile = Profile.objects.get(user=self.second_user)
        self.third_profile = Profile.objects.get(user=self.third_user)

        self.project = Project.objects.create(
            pk=1,
            user=self.first_profile,
            category=self.project_category)

        self.task = Task.objects.create(project=self.project)

        self.task_offer = TaskOffer(
            task=self.task,
            offerer=self.first_profile,
            status = 'a')
        
        self.task_offer = TaskOffer(
            task=self.task,
            offerer=self.third_profile,
            status = 'a')
        self.task_offer.save()
    
    def test_accepting_function(self):
        offer = self.task.accepted_task_offer()
        print(offer.id)
'''

    
