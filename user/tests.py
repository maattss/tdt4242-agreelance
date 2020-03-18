from django.test import TestCase
from projects.models import ProjectCategory
from faker import Faker
from factory.fuzzy import FuzzyText
from .forms import SignUpForm
import string
from allpairspy import AllPairs
from collections import OrderedDict

# Boundary value tests for sign-up page
class TestSignupPageBoundary(TestCase):
    def setUp(self):
        fake = Faker() # Generate fake data using a faker generator

        # Boundary values for number of characters in fields
        self.above_max_username = FuzzyText(length=151)
        self.below_max_username = FuzzyText(length=150)
        self.normal_username = fake.user_name()
        
        self.above_max_email = FuzzyText(length=245, suffix="@gmail.com")
        self.below_max_email = FuzzyText(length=244, suffix="@gmail.com")
        self.above_min_email = FuzzyText(length=1, suffix="@gmail.com")
        self.below_min_email = FuzzyText(length=1)
        self.normal_email = fake.email()

        self.above_max_password = FuzzyText(length=4097)
        self.below_max_password = FuzzyText(length=4096)
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
        password = self.above_max_password.fuzz()
        
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
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())
    
    def test_below_max(self):
        email = self.below_max_email.fuzz()
        password = self.below_max_password.fuzz()
        
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
        data = {
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
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())

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
        password_1 = FuzzyText(length=5000).fuzz()
        password_2 = FuzzyText(length=4).fuzz()
        password_3 = FuzzyText(length=16, chars=string.digits).fuzz()
        categories = []

        declined_parameters = [
            [username_1, username_2, username_3],
            [textfield_30_1, textfield_30_2],
            [textfield_50_1, textfield_50_2],
            [email_1, email_2],
            [email_1, email_2],
            [password_1, password_2, password_3],
            [password_1, password_2, password_3],
            [categories]
        ]

        # Generate all possible combinations
        self.declined_combinations = list(AllPairs(declined_parameters))

        self.declined_parameters_dict = OrderedDict({
            "username": [username_1, username_2, username_3],
            "textfield_30": [textfield_30_1, textfield_30_2],
            "textfield_50": [textfield_50_1, textfield_50_2],
            "email": [email_1, email_2],
            "password": [password_1, password_2, password_3],
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

            # Using subtest to prevent return of test failure immediately,
            # possibly before all combinations are tested!
            with self.subTest(form=form):
                self.assertFalse(form.is_valid())

    # Special test case when emails are not equal
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
        self.assertTrue(form.is_valid()) # Bug in form, this should be false
    
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
    
"""
# DEPRECATED - 2-way domain tests of the sign-up page - DEPRECATED
class TestSignupPageDomainDeprecated(TestCase):
    def setUp(self):
        fake = Faker() # Generate fake data using a faker generator

        # Configure values used in the test cases
        self.approved_textfield = FuzzyText(length=20)
        self.declined_textfield = ""

        self.approved_email_1 = fake.email()
        self.approved_email_2 = fake.email()
        self.declined_email = FuzzyText(length=245, suffix="@gmail.com")

        self.approved_password_1 = fake.password()
        self.approved_password_2 = fake.password()
        self.declined_password = FuzzyText(length=4097)

        self.approved_categories = [ProjectCategory.objects.create(pk=1)]
        self.declined_categories = []

    def test_first_case(self):
        data = {
            'username': self.declined_textfield,
            'first_name': self.declined_textfield,
            'last_name': self.declined_textfield,
            'categories': self.approved_categories,
            'company': self.declined_textfield,
            'email': self.approved_email_1,
            'email_confirmation': self.approved_email_2,
            'password1': self.declined_password.fuzz(),
            'password2': self.declined_password.fuzz(),
            'phone_number': self.declined_textfield,
            'country': self.declined_textfield,
            'state': self.declined_textfield,
            'city': self.declined_textfield,
            'postal_code': self.declined_textfield,
            'street_address': self.declined_textfield,   
        }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())
    
    def test_second_case(self):
        data = {
            'username': self.approved_textfield.fuzz(),
            'first_name': self.approved_textfield.fuzz(),
            'last_name': self.approved_textfield.fuzz(),
            'categories': self.approved_categories,
            'company': self.approved_textfield.fuzz(),
            'email': self.declined_email,
            'email_confirmation': self.declined_email,
            'password1': self.approved_password_1,
            'password2': self.approved_password_2,
            'phone_number': self.approved_textfield.fuzz(),
            'country': self.approved_textfield.fuzz(),
            'state': self.approved_textfield.fuzz(),
            'city': self.approved_textfield.fuzz(),
            'postal_code': self.approved_textfield.fuzz(),
            'street_address': self.approved_textfield.fuzz(),   
        }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())

    def test_third_case(self):
        data = {
            'username': self.approved_textfield.fuzz(),
            'first_name': self.approved_textfield.fuzz(),
            'last_name': self.approved_textfield.fuzz(),
            'categories': self.approved_categories,
            'company': self.approved_textfield.fuzz(),
            'email': self.approved_email_1,
            'email_confirmation': self.approved_email_1,
            'password1': self.approved_password_1,
            'password2': self.approved_password_1,
            'phone_number': self.approved_textfield.fuzz(),
            'country': self.approved_textfield.fuzz(),
            'state': self.approved_textfield.fuzz(),
            'city': self.approved_textfield.fuzz(),
            'postal_code': self.approved_textfield.fuzz(),
            'street_address': self.approved_textfield.fuzz(),   
        }
        form = SignUpForm(data)
        self.assertTrue(form.is_valid())
"""