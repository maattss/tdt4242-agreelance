from django.test import TestCase, RequestFactory
from projects.models import ProjectCategory
from faker import Faker
from user.forms import ReviewForm
from django.contrib.auth.models import User
from projects.models import Project, Task, TaskOffer
from user.models import Profile, Review
from user.views import review
from django.core.exceptions import ObjectDoesNotExist

# Integration and system tests for reviews, i.e. ratings and comments features
class TestReviewImplementation(TestCase):
    def setUp(self):
        self.fake = Faker() # Generate fake data using a faker generator

        self.factory = RequestFactory() # Mock request objects
        self.project_category = ProjectCategory.objects.create(pk=1)
        
        self.first_user = User.objects.create_user(
            pk=1,
            username=self.fake.user_name(),
            password=self.fake.password()
        )
        self.second_user = User.objects.create_user(
            pk=2,
            username=self.fake.user_name(),
            password=self.fake.password()
        )
        self.third_user = User.objects.create_user(
            pk=3,
            username=self.fake.user_name(),
            password=self.fake.password()
        )
        self.fourth_user = User.objects.create_user(
            pk=4,
            username=self.fake.user_name(),
            password=self.fake.password()
        )
        
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
            status='a'
        )
        self.second_task_offer = TaskOffer.objects.create(
            task=self.first_task,
            offerer=self.third_profile,
            status='a'
        )
        self.first_review = Review.objects.create(
            pk=1,
            reviewer=self.first_profile,
            reviewed=self.second_user,
            rating=self.fake.random_int(min=1, max=5),
            comment=self.fake.sentence(nb_words=10)
        )

    # Test if first_review from setUp is stored in the database
    def test_get_review(self):
        review = Review.objects.get(pk = 1)
        self.assertEquals(review, self.first_review)

    # First_user and third user have worked together and no review exists in the database. 
    # The request should be stored in database.
    def test_valid_review(self):
        rating = self.fake.random_int(min=1, max=5)
        comment = self.fake.sentence(nb_words=10)
        insert_review(self, self.first_user, self.third_user, rating, comment)
        db_review = get_review(self, self.first_profile, self.third_user, rating, comment)
        self.assertTrue(db_review)

    # First_user and fourth_user haven't worked together. 
    # The request should not be stored since confirm_work_relationship returns False
    def test_no_relationship_review(self):
        rating = self.fake.random_int(min=1, max=5)
        comment = self.fake.sentence(nb_words=10)
        insert_review(self, self.first_user, self.fourth_user, rating, comment)
        db_review = get_review(self, self.first_profile, self.fourth_user, rating, comment)
        self.assertFalse(db_review)

    # There is already a review from first_user on second_user from setUp. 
    # The request should not be stored since confirm_duplicate_review returns True
    def test_duplicate_review(self):
        rating = self.fake.random_int(min=1, max=5)
        comment = self.fake.sentence(nb_words=10)
        insert_review(self, self.first_user, self.second_user, rating, comment)
        db_review = get_review(self, self.first_profile, self.second_user, rating, comment)
        self.assertFalse(db_review)

    # Test making a review with invalid reviewed_id
    def test_invalid_reviewed_user(self):
        request = self.factory.post('/user/set_review/', {
            'rating': self.fake.random_int(min=1, max=5),
            'comment': self.fake.sentence(nb_words=10)
        })
        request.user = self.first_user
        invalid_reviewed_user_id = self.fake.random_int(min=10, max=999)
        response = None
        try:    
            response = review(request, invalid_reviewed_user_id)
        except:
            pass
        self.assertFalse(response)
    
    # Test sql injection vulnerability by checking if the entire string is stored as a data
    def test_strange_comment(self):
        rating = self.fake.random_int(min=1, max=5)
        comment = '"select * from user_review where 1=1"'
        insert_review(self, self.first_user, self.third_user, rating, comment)
        db_review = get_review(self, self.first_profile, self.third_user, rating, comment)
        self.assertTrue(db_review)
    
    def test_above_max_rating(self):
        data = {
            'rating': self.fake.random_int(min=1, max=999),
            'comment': self.fake.sentence(nb_words=10),
        }
        form = ReviewForm(data)
        self.assertFalse(form.is_valid())

    def test_negative_rating(self):
        data = {
            'rating': self.fake.random_int(min=-999, max=-1),
            'comment': self.fake.sentence(nb_words=10),
        }
        form = ReviewForm(data)
        self.assertFalse(form.is_valid())
    
# Helper function
def insert_review(self, reviewer_user, reviewed_user, rating, comment):
    request = self.factory.post('/user/set_review/', {
        'rating': rating,
        'comment': comment
    })
    request.user = reviewer_user
    review(request, reviewed_user.id) 

# Helper function
def get_review(self, reviewer_profile, reviewed_user, rating, comment):
    db_review = None
    try:
        db_review = Review.objects.get(
            reviewer = reviewer_profile,
            reviewed = reviewed_user,
            rating = rating,
            comment = comment)
    except ObjectDoesNotExist:
        pass
    return db_review
    