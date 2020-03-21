from django.test import TestCase, RequestFactory
from projects.models import ProjectCategory
from faker import Faker
from user.forms import ReviewForm
from django.contrib.auth.models import User
from projects.models import Project, Task, TaskOffer
from user.models import Profile, Review
from user.views import review

# Integration and system tests for reviews - rating and comment features
class TestReviewImplementation(TestCase):
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
            pk=3,
            username=fake.user_name(),
            password=fake.password())
        
        self.fourth_user = User.objects.create_user(
            pk=4,
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
        self.second_task = Task.objects.create(project=self.project, status='dd')
        
        self.first_task_offer = TaskOffer.objects.create(
            task=self.first_task,
            offerer=self.second_profile,
            status='a')
        
        self.second_task_offer = TaskOffer.objects.create(
            task=self.first_task,
            offerer=self.third_profile,
            status='a')
        
        self.first_review = Review.objects.create(
                pk=1,
                reviewer=self.first_profile,
                reviewed=self.second_user,
                rating=3,
                comment='It was okay')
        
        self.over_valid_rating = 999
        self.negative_rating = -999

    # first_user and third user have worked together and no review exists in the database. The request should be stored in database.
    def test_valid_review(self):
        request = self.factory.post('/user/set_review/', {
            'rating': 5,
            'comment': 'Very good review!'
        })
        request.user = self.first_user
        response = review(request, self.third_user.id)
        db_review = None
        try:
            db_review = Review.objects.get(reviewer=self.first_profile,
                reviewed=self.third_user,
                rating=5,
                comment='Very good review!')
        except:
            pass
        self.assertTrue(db_review)

    # first_user and fourth_user haven't worked together. The request should not be stored since confirm_work_relationship returns False
    def test_no_relationship_review(self):
        request = self.factory.post('/user/set_review/', {
            'rating': 1,
            'comment': 'This shouldnt be possible'
        })
        request.user = self.first_user
        response = review(request, self.fourth_user.id)
        db_review = None
        try:
            db_review = Review.objects.get(reviewer=self.first_profile,
                reviewed=self.fourth_user,
                rating=1,
                comment='This shouldnt be possible')
        except:
            pass
        self.assertFalse(db_review)


    # There is already a review from first_user on second_user from setUp. The request should not be stored since confirm_duplicate_review returns True
    def test_duplicate_review(self):
        request = self.factory.post('/user/set_review/', {
            'rating': 2,
            'comment': 'This shouldnt be possible either'
        })
        request.user = self.first_user # Set logged in user
        response = review(request, self.second_user.id)
        db_review = None
        try:
            db_review = Review.objects.get(reviewer=self.first_profile,
                reviewed=self.second_user,
                rating=2,
                comment='This shouldnt be possible either')
        except:
            pass
        self.assertFalse(db_review)
    
    def test_above_max_rating(self):
        data = {
            'rating': self.over_valid_rating,
            'comment': 'Rating over 5 shouldnt be possible',

        }
        form = ReviewForm(data)
        self.assertFalse(form.is_valid())

    def test_negative_rating(self):
        data = {
            'rating': self.negative_rating,
            'comment': 'Under 1 shouldnt be possible',

        }
        form = ReviewForm(data)
        self.assertFalse(form.is_valid())

    # Test making a review with invalid reviewed_id
    def test_invalid_reviewed_user(self):
        request = self.factory.post('/user/set_review/', {
            'rating': 2,
            'comment': 'Testing'
        })
        request.user = None
        response = None
        try:    
            request.user = self.first_user
            response = review(request, 87678)
        except:
            pass

        self.assertFalse(response)
    
    # Test sql injection vulnerability by checking if the entire string is stored as a data
    def test_strange_comment(self):
        request = self.factory.post('/user/set_review/', {
            'rating': 5,
            'comment': '"select * from user_review where 1=1"'
        })
        request.user = self.first_user
        review(request, self.third_user.id)
        db_review = None
        try:
            db_review = Review.objects.get(reviewer=self.first_profile,
                reviewed=self.third_user,
                rating=5,
                comment='"select * from user_review where 1=1"')
        except:
            pass
        self.assertTrue(db_review)