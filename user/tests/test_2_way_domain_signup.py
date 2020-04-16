from django.test import TestCase
from projects.models import ProjectCategory
from faker import Faker
from factory.fuzzy import FuzzyText
from user.forms import SignUpForm
import string
from allpairspy import AllPairs
from collections import OrderedDict
from unittest import skip

# 2-way domain tests of the sign-up page
class TestSignupPageDomain(TestCase):
    def setUp(self):
        fake = Faker() # Generate fake data using a faker generator

        # Configure values used in the success test case
        self.approved_username = FuzzyText(length=20).fuzz()
        self.approved_textfield_30 = FuzzyText(length=20).fuzz()
        self.approved_textfield_50 = FuzzyText(length=40).fuzz()
        self.approved_email_1 = fake.email()
        self.approved_email_2 = fake.email()
        self.approved_password_1 = fake.password()
        self.approved_password_2 = fake.password()
        self.approved_categories = [ProjectCategory.objects.create(pk=1)]
        
        # Configure declined parameters for use in the test cases
        username_1 = ""
        username_2 = FuzzyText(length=50, chars=string.punctuation).fuzz() # Special charaters
        username_3 = FuzzyText(length=151).fuzz()
        textfield_30_1 = ""
        textfield_30_2 = FuzzyText(length=40).fuzz()
        textfield_50_1 = ""
        textfield_50_2 = FuzzyText(length=60).fuzz()
        email_1 = FuzzyText(length=245, suffix="@gmail.com").fuzz()
        email_2 = FuzzyText(length=20).fuzz()
        password_1 = FuzzyText(length=4).fuzz()
        password_2 = FuzzyText(length=16, chars=string.digits).fuzz()
        categories = []

        declined_parameters = [
            [username_1, username_2, username_3],
            [textfield_30_1, textfield_30_2],
            [textfield_50_1, textfield_50_2],
            [email_1, email_2],
            [email_1, email_2],
            [password_1, password_2],
            [password_1, password_2],
            [categories]
        ]

        # Generate all possible combinations
        self.declined_combinations = list(AllPairs(declined_parameters))

        self.declined_parameters_dict = OrderedDict({
            "username": [username_1, username_2, username_3],
            "textfield_30": [textfield_30_1, textfield_30_2],
            "textfield_50": [textfield_50_1, textfield_50_2],
            "email": [email_1, email_2],
            "password": [password_1, password_2],
            "categories": [categories]
        })

    # All combinations
    def test_declined_combinations(self):
        for _, pairs in enumerate(AllPairs(self.declined_parameters_dict)):
            data = {
                'username': pairs.username,
                'first_name': pairs.textfield_30,
                'last_name': pairs.textfield_30,
                'categories': pairs.categories,
                'company': pairs.textfield_30,
                'email': pairs.email,
                'email_confirmation': pairs.email,
                'password1': pairs.password,
                'password2': pairs.password,
                'phone_number': pairs.textfield_50,
                'country': pairs.textfield_50,
                'state': pairs.textfield_50,
                'city': pairs.textfield_50,
                'postal_code': pairs.textfield_50,
                'street_address': pairs.textfield_50
            }
            form = SignUpForm(data)

            # Using sub test to prevent return of test failure immediately,
            # possibly before all combinations are tested!
            with self.subTest(form=form):
                self.assertFalse(form.is_valid())

    # Special test case when emails are not equal
    @skip("Form should not be valid when emails in form are not equal")
    def test_different_email(self):
        data = {
            'username': self.approved_username ,
            'first_name': self.approved_textfield_30,
            'last_name': self.approved_textfield_30,
            'categories': self.approved_categories,
            'company': self.approved_textfield_30,
            'email': self.approved_email_1,
            'email_confirmation': self.approved_email_2,
            'password1': self.approved_password_1,
            'password2': self.approved_password_1,
            'phone_number': self.approved_textfield_50,
            'country': self.approved_textfield_50,
            'state': self.approved_textfield_50,
            'city': self.approved_textfield_50,
            'postal_code': self.approved_textfield_50,
            'street_address': self.approved_textfield_50   
        }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())
    
    # Special test case when passwords are not equal
    def test_different_passwords(self):
        data = {
            'username': self.approved_username ,
            'first_name': self.approved_textfield_30,
            'last_name': self.approved_textfield_30,
            'categories': self.approved_categories,
            'company': self.approved_textfield_30,
            'email': self.approved_email_1,
            'email_confirmation': self.approved_email_1,
            'password1': self.approved_password_1,
            'password2': self.approved_password_2,
            'phone_number': self.approved_textfield_50,
            'country': self.approved_textfield_50,
            'state': self.approved_textfield_50,
            'city': self.approved_textfield_50,
            'postal_code': self.approved_textfield_50,
            'street_address': self.approved_textfield_50    
        }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())

    # Test case when form is valid 
    def test_valid_form(self):
        data = {
            'username': self.approved_username ,
            'first_name': self.approved_textfield_30,
            'last_name': self.approved_textfield_30,
            'categories': self.approved_categories,
            'company': self.approved_textfield_30,
            'email': self.approved_email_1,
            'email_confirmation': self.approved_email_1,
            'password1': self.approved_password_1,
            'password2': self.approved_password_1,
            'phone_number': self.approved_textfield_50,
            'country': self.approved_textfield_50,
            'state': self.approved_textfield_50,
            'city': self.approved_textfield_50,
            'postal_code': self.approved_textfield_50,
            'street_address': self.approved_textfield_50  
        }
        form = SignUpForm(data)
        self.assertTrue(form.is_valid())