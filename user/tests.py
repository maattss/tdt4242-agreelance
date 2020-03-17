from django.test import TestCase
from projects.models import ProjectCategory
from faker import Faker
from factory.fuzzy import FuzzyText
from .forms import SignUpForm
from .models import Profile, Review
from django.contrib.auth.models import AnonymousUser, User
from projects.models import ProjectCategory, Project, Task, TaskOffer
from .review_functions import confirm_duplicate_review, confirm_work_relationship

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
        
class TestReviewImplementation(TestCase):
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

        self.third_user = User.objects.create_user(
            pk=3,
            username=fake.user_name(),
            password=fake.password())
        
        self.first_profile = Profile.objects.get(user=self.first_user)
        self.second_profile = Profile.objects.get(user=self.second_user)
        self.third_profile = Profile.objects.get(user=self.third_user)


        self.project = Project.objects.create(
            pk=1,
            user=self.first_profile,
            category=self.project_category)
        
        
        self.first_task = Task.objects.create(project=self.project, status='ps')

        self.task_offer = TaskOffer.objects.create(
            task=self.first_task,
            offerer=self.second_profile,
            status='a')

        if(confirm_work_relationship(self.first_profile, self.second_user) and not confirm_duplicate_review(self.first_profile, self.second_user)):
            self.first_review = Review.objects.create(
                pk=1,
                reviewer=self.first_profile,
                reviewed=self.second_user,
                rating=3,
                comment='It was okay',
            )

        if(confirm_work_relationship(self.first_profile, self.second_user) and not confirm_duplicate_review(self.first_profile, self.second_user)):
            self.second_review = Review.objects.create(
                pk=2,
                reviewer=self.first_profile,
                reviewed=self.second_user,
                rating=5,
                comment='I reviewed you again!',
            )
        else:
            self.second_review = None
        
    def test_valid_review(self):
#Checking for a review with the values entered earlier should be found in the database. Test passes if the data in the database equals what is entered in setUp
        db_review = None
        try:
            db_review = Review.objects.get(pk=1, reviewer=self.first_profile,
                reviewed=self.second_user,
                rating=3,
                comment='It was okay')
        except:
            pass
        self.assertEqual(self.first_review, db_review)

#db_review should be None since confirm_working_relationship returns false.
    def test_no_relationship_review(self):
        db_review = None
        try:
            db_review = Review.objects.get(
                reviewer=self.first_profile,
                reviewed=self.third_user)
        except:
            pass
        self.assertFalse(db_review)

#Second_review should be None since confirm_duplicate_review returns true.
    def test_duplicate_review(self):
        self.assertFalse(self.second_review)








        