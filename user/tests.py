from django.test import TestCase
from faker import Faker

# Boundary value tests for sign-up page
class TestSignupPageBoundary(TestCase):
    def setUp(self):
        # Create and initialize a faker generator, which can generate different types of fake data
        self.fake = Faker()
        self.fake.seed_instance(123456)

        # Boundary values for number of characters in fields
        self.max_name = 150
        self.min_name = 1
        self.max_password = 4096
        self.min_password = 8
        self.max_other_50 = 50
        self.max_other_30 = 30
        self.min_other = 1
    
    def test_min_values(self):
        
        # All data not related to user profile can be empty?
        data = {
            'username': self.fake.user_name(),
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            'categories': 1, # TODO: Random generate?
            'company': self.fake.company(),
            'email': self.fake.ascii_free_email(),
            'email_confirmation': self.fake.ascii_free_email(),
            'password1': self.fake.password(),
            'password2': self.fake.password(),
            'phone_number': self.fake.phone_number(),
            'country': self.fake.country(),
            'state': self.fake.state(),
            'city': self.fake.city(),
            'postal_code': self.fake.postalcode(),
            'street_adress': self.fake.address(),
            
        }
        print("Data", data)
    
    def test_max_values(self):
        print("heyhey")


# 2-way domain tests of the sugn-up page
class TestSignupPageDomain(TestCase):
    # TODO: Implement test
    def setUp(self):
        self.name = "tests"
        