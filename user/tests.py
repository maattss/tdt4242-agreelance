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