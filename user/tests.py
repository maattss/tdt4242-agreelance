from django.test import TestCase
from projects.models import ProjectCategory
from faker import Faker
from factory.fuzzy import FuzzyText, FuzzyChoice
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
        self.categories = [ProjectCategory.objects.create(pk=1), 
            ProjectCategory.objects.create(pk=2), ProjectCategory.objects.create(pk=3)]
    
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
            'categories': self.categories,
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
        