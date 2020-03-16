<<<<<<< HEAD
from django.test import TestCase, Client
from projects.views import project_view, get_user_task_permissions
from projects.models import ProjectCategory, Project, Task, TaskOffer
from .views import review
from user.models import Profile, Review

from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase

class Test_review_view(TestCase):
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
        self.profile2 = Profile.objects.get(user=self.second_user)

        self.project = Project.objects.create(
            pk=1,
            user=self.profile,
            category=self.pCategory)

        self.task = Task.objects.create(project=self.project, status = 'ps')

        self.task_offer = TaskOffer(
            task=self.task,
            offerer=self.profile2)
        self.task_offer.save()

        self.review = Review.objects.create(
            reviewer = self.profile,
            reviewed = self.second_user
            )
        
    def test_review_response(self):
        #Trying to test posting a review. Doesn't work properly
        request = self.factory.post('/user/set_review/'+ str(self.second_user.id), {
            'rating': '3 - Okay',
            'comment': 'Not bad',
        })
        request.user = self.first_user
        response = review(request, 1)
        self.assertEqual(response.status_code, 200)
    '''
    #Tests if /user/set_review/<user.id>/ works
    def test_review_view_url_exists(self):
        response = self.client.get('/user/set_review/'+ str(self.second_user.id)+ '/')
        self.assertEqual(response.status_code, 200)
    
    #Tests if /user/<user.id>/ works
    def test_userpage_view_url_exists(self):
        response = self.client.get('/user/'+ str(self.second_user.id)+ '/')
        self.assertEqual(response.status_code, 200)
    '''
=======
from django.test import TestCase
from projects.models import ProjectCategory
from faker import Faker
from factory.fuzzy import FuzzyText
from .forms import SignUpForm

# Boundary value tests for sign-up page
class TestSignupPageBoundary(TestCase):
    def setUp(self):
        # Boundary values for number of characters in fields
        self.max_username = FuzzyText(length=150)
        self.max_email = FuzzyText(length=244, suffix="@gmail.com")
        self.min_email = FuzzyText(length=1, suffix="@gmail.com")
        self.max_password = FuzzyText(length=4096)
        self.min_password = FuzzyText(length=8)
        self.max_50 = FuzzyText(length=50)
        self.max_30 = FuzzyText(length=30)
        self.min = FuzzyText(length=1)
        self.min_categories = [ProjectCategory.objects.create(pk=1)]
        self.categories = [ProjectCategory.objects.create(pk=2), 
            ProjectCategory.objects.create(pk=3), ProjectCategory.objects.create(pk=4)]
    
    def test_max_values(self):
        email = self.max_email.fuzz()
        password = self.max_password.fuzz()
        
        data = {
            'username': self.max_username.fuzz(),
            'first_name': self.max_30.fuzz(),
            'last_name': self.max_30.fuzz(),
            'categories': self.categories,
            'company': self.max_30.fuzz(),
            'email': email,
            'email_confirmation': email,
            'password1': password,
            'password2': password,
            'phone_number': self.max_50.fuzz(),
            'country': self.max_50.fuzz(),
            'state': self.max_50.fuzz(),
            'city': self.max_50.fuzz(),
            'postal_code': self.max_50.fuzz(),
            'street_address': self.max_50.fuzz(),   
        }
        form = SignUpForm(data)
        self.assertTrue(form.is_valid())
    
    def test_min_values(self):
        email = self.min_email.fuzz()
        password = self.min_password.fuzz()
        
        data = {
            'username': self.min.fuzz(),
            'first_name': self.min.fuzz(),
            'last_name': self.min.fuzz(),
            'categories': self.min_categories,
            'company': self.min.fuzz(),
            'email': email,
            'email_confirmation': email,
            'password1': password,
            'password2': password,
            'phone_number': self.min.fuzz(),
            'country': self.min.fuzz(),
            'state': self.min.fuzz(),
            'city': self.min.fuzz(),
            'postal_code': self.min.fuzz(),
            'street_address': self.min.fuzz(),   
        }
        form = SignUpForm(data)
        self.assertTrue(form.is_valid())

# 2-way domain tests of the sign-up page
class TestSignupPageDomain(TestCase):
    # TODO: Implement test
    def setUp(self):
        self.name = "tests"
        
>>>>>>> master
