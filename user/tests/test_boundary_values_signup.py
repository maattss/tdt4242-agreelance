from django.test import TestCase
from projects.models import ProjectCategory
from faker import Faker
from factory.fuzzy import FuzzyText
from user.forms import SignUpForm
import copy
from unittest import skip

# Boundary value tests for sign-up page
class TestSignupPageBoundary(TestCase):
    def setUp(self):
        fake = Faker() # Generate fake data using a faker generator

        self.above_max_username = FuzzyText(length=151)
        self.below_max_username = FuzzyText(length=150)
        self.normal_username = fake.user_name()
        
        self.above_max_email = FuzzyText(length=245, suffix="@gmail.com")
        self.below_max_email = FuzzyText(length=244, suffix="@gmail.com")
        self.above_min_email = FuzzyText(length=1, suffix="@gmail.com")
        self.below_min_email = FuzzyText(length=1)
        self.normal_email = fake.email()

        self.above_min_password = FuzzyText(length=8)
        self.below_min_password = FuzzyText(length=7)
        self.normal_password = fake.password()

        self.above_max_50 = FuzzyText(length=51)
        self.below_max_50 = FuzzyText(length=50)

        self.above_max_30 = FuzzyText(length=31)
        self.below_max_30 = FuzzyText(length=30)
        
        self.normal = FuzzyText(length=20)
        self.above_min = FuzzyText(length=1)
        self.below_min = ""

        self.categories = [ProjectCategory.objects.create(pk=1), 
            ProjectCategory.objects.create(pk=2), ProjectCategory.objects.create(pk=3)]
        self.above_min_categories = [ProjectCategory.objects.create(pk=4)]
        self.below_min_categories = []
        
    
    def test_above_max(self):
        email = self.above_max_email.fuzz()
        password = self.normal_password
        
        data = {
            'username': self.above_max_username.fuzz(),
            'first_name': self.above_max_30.fuzz(),
            'last_name': self.above_max_30.fuzz(),
            'categories': self.categories,
            'company': self.above_max_30.fuzz(),
            'email': email,
            'email_confirmation': email,
            'password1': password,
            'password2': password,
            'phone_number': self.above_max_50.fuzz(),
            'country': self.above_max_50.fuzz(),
            'state': self.above_max_50.fuzz(),
            'city': self.above_max_50.fuzz(),
            'postal_code': self.above_max_50.fuzz(),
            'street_address': self.above_max_50.fuzz(),   
        }
        valid_data = get_valid_data(self)
        for item in data.items():
            valid_data_copy = copy.copy(valid_data)
            if item[0] == "categories": # No max limit for categories
                continue
            elif item[0] == "email" or item[0] == "email_confirmation": # Special case for email
                valid_data_copy["email"] = item[1]
                valid_data_copy["email_confirmation"] = item[1]
                form = SignUpForm(valid_data_copy)
                with self.subTest(form=form):
                    self.assertFalse(form.is_valid())
            elif item[0] == "password1" or item[0] == "password2": # Special case for password
                valid_data_copy["password1"] = item[1]
                valid_data_copy["password2"] = item[1]
                form = SignUpForm(valid_data_copy)
                with self.subTest(form=form):
                    # Password has a limit on 4096 characters, i.e. this test should fail
                    self.assertTrue(form.is_valid())
            else:
                valid_data_copy[item[0]] = item[1]
                form = SignUpForm(valid_data_copy)
                with self.subTest(form=form):
                    self.assertFalse(form.is_valid())
    
    def test_below_max(self):
        email = self.below_max_email.fuzz()
        password = self.normal_password
        
        data = {
            'username': self.below_max_username.fuzz(),
            'first_name': self.below_max_30.fuzz(),
            'last_name': self.below_max_30.fuzz(),
            'categories': self.categories,
            'company': self.below_max_30.fuzz(),
            'email': email,
            'email_confirmation': email,
            'password1': password,
            'password2': password,
            'phone_number': self.below_max_50.fuzz(),
            'country': self.below_max_50.fuzz(),
            'state': self.below_max_50.fuzz(),
            'city': self.below_max_50.fuzz(),
            'postal_code': self.below_max_50.fuzz(),
            'street_address': self.below_max_50.fuzz(),   
        }
        form = SignUpForm(data)
        self.assertTrue(form.is_valid())

    def test_normal_values(self):
        data = get_valid_data(self)
        form = SignUpForm(data)
        self.assertTrue(form.is_valid())
    
    def test_above_min(self):
        email = self.above_min_email.fuzz()
        password = self.above_min_password.fuzz()
        
        data = {
            'username': self.above_min.fuzz(),
            'first_name': self.above_min.fuzz(),
            'last_name': self.above_min.fuzz(),
            'categories': self.above_min_categories,
            'company': self.above_min.fuzz(),
            'email': email,
            'email_confirmation': email,
            'password1': password,
            'password2': password,
            'phone_number': self.above_min.fuzz(),
            'country': self.above_min.fuzz(),
            'state': self.above_min.fuzz(),
            'city': self.above_min.fuzz(),
            'postal_code': self.above_min.fuzz(),
            'street_address': self.above_min.fuzz(),   
        }
        form = SignUpForm(data)
        self.assertTrue(form.is_valid())
    
    def test_below_min(self):
        email = self.below_min_email.fuzz()
        password = self.below_min_password.fuzz()
        
        data = {
            'username': self.below_min,
            'first_name': self.below_min,
            'last_name': self.below_min,
            'categories': self.below_min_categories,
            'company': self.below_min,
            'email': email,
            'email_confirmation': email,
            'password1': password,
            'password2': password,
            'phone_number': self.below_min,
            'country': self.below_min,
            'state': self.below_min,
            'city': self.below_min,
            'postal_code': self.below_min,
            'street_address': self.below_min,   
        }
        valid_data = get_valid_data(self)
        for item in data.items():
            valid_data_copy = copy.copy(valid_data)
            if item[0] == "company": # Company field can be empty
                continue      
            elif item[0] == "email" or item[0] == "email_confirmation": # Special case for email
                valid_data_copy["email"] = item[1]
                valid_data_copy["email_confirmation"] = item[1]
                form = SignUpForm(valid_data_copy)
                with self.subTest(form=form):
                    self.assertFalse(form.is_valid())
            elif item[0] == "password1" or item[0] == "password2": # Special case for password
                valid_data_copy["password1"] = item[1]
                valid_data_copy["password2"] = item[1]
                form = SignUpForm(valid_data_copy)
                with self.subTest(form=form):
                    self.assertFalse(form.is_valid())
            else:
                valid_data_copy[item[0]] = item[1]
                form = SignUpForm(valid_data_copy)
                with self.subTest(form=form):
                    self.assertFalse(form.is_valid())

def get_valid_data(self):
    return {
            'username': self.normal_username,
            'first_name': self.normal.fuzz(),
            'last_name': self.normal.fuzz(),
            'categories': self.categories,
            'company': self.normal.fuzz(),
            'email': self.normal_email,
            'email_confirmation': self.normal_email,
            'password1': self.normal_password,
            'password2': self.normal_password,
            'phone_number': self.normal.fuzz(),
            'country': self.normal.fuzz(),
            'state': self.normal.fuzz(),
            'city': self.normal.fuzz(),
            'postal_code': self.normal.fuzz(),
            'street_address': self.normal.fuzz(),   
    }