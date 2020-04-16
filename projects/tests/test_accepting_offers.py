from django.test import TestCase
from projects.views import project_view
from projects.models import ProjectCategory, Project, Task, TaskOffer
from user.models import Profile
from faker import Faker
from django.contrib.auth.models import User
from django.test import RequestFactory
from django.http import Http404
from unittest import skip

# Accept offer output coverage tests
class TestAcceptingOffers(TestCase):
    def setUp(self):
        self.fake = Faker() # Generate fake data using a faker generator
        
        self.factory = RequestFactory()
        self.project_category = ProjectCategory.objects.create(pk=1)

        # First user is project owner and second user creates offer
        self.first_user = User.objects.create_user(
            pk=1,
            username=self.fake.user_name(),
            password=self.fake.password())
        self.second_user = User.objects.create_user(
            pk=2,
            username=self.fake.user_name(),
            password=self.fake.password())
        
        self.first_profile = Profile.objects.get(user=self.first_user)
        self.second_profile = Profile.objects.get(user=self.second_user)

        self.project = Project.objects.create(
            pk=1,
            user=self.first_profile,
            category=self.project_category)

        self.first_task = Task.objects.create(project=self.project)

        self.first_task_offer = TaskOffer(
            task=self.first_task,
            offerer=self.second_profile,
            status = 'o')
        
        self.first_task_offer.save()

    def test_accepted_output(self):
        status = "a"
        feedback = self.fake.sentence(nb_words=6)
        post_response(self, status, feedback)
        offer = TaskOffer.objects.get(task_id=self.first_task.pk)

        self.assertEqual(offer.status, status)
        self.assertEqual(offer.feedback, feedback)
    
    @skip("Should not be possible to submit a pending response")
    def test_pending_output(self):
        status = "p"
        feedback = self.fake.sentence(nb_words=6)
        post_response(self, status, feedback)
        offer = TaskOffer.objects.get(task_id=self.first_task.pk)

        self.assertNotEqual(offer.status, status)
        self.assertNotEqual(offer.feedback, feedback)

    def test_declined_output(self):
        status = "d"
        feedback = self.fake.sentence(nb_words=6)
        post_response(self, status, feedback)
        offer = TaskOffer.objects.get(task_id=self.first_task.pk)

        self.assertEqual(offer.status, status)
        self.assertEqual(offer.feedback, feedback)
   
    def test_not_existing_offer_output(self):
        status = "a"
        feedback = self.fake.sentence(nb_words=6)
        
        request = self.factory.post('/projects/' + str(self.first_task.pk) + "/", {
            'status': status,
            'feedback': feedback,
            'taskofferid': self.fake.random_int(min=100),
            'offer_response': ''
        })
        request.user = self.first_user
        success = True
        try:
            project_view.project_view(request, self.project.pk)
        except Http404:
            success = False
        self.assertFalse(success)

def post_response(self, status, feedback):
    request = self.factory.post('/projects/' + str(self.first_task.pk) + "/", {
        'status': status,
        'feedback': feedback,
        'taskofferid': self.first_task_offer.pk,
        'offer_response': ''
    })
    request.user = self.first_user
    project_view.project_view(request, self.project.pk)