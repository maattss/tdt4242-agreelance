from django.test import TestCase, RequestFactory
from projects.models import Task, ProjectCategory, Project, TaskOffer, Team
from projects.views import task_view
from user.models import Profile, User
from faker import Faker
from django.core.files.uploadedfile import SimpleUploadedFile

class TestTaskView(TestCase):
    def setUp(self):
        self.fake = Faker() # Generate fake data using a faker generator

        self.factory = RequestFactory()
        
        self.project_category = ProjectCategory.objects.create(pk=1)

        self.user = User.objects.create_user(
            pk=1,
            username=self.fake.user_name(),
            password=self.fake.password())
        self.second_user = User.objects.create_user(
            pk=2,
            username=self.fake.user_name(),
            password=self.fake.password())
        
        self.profile = Profile.objects.get(user=self.user)
        self.second_profile = Profile.objects.get(user=self.second_user)
        

        self.project = Project.objects.create(
            pk=1,
            user=self.profile,
            category=self.project_category)
        self.task = Task.objects.create(
            id=1,
            project=self.project
        )

        self.task_offer = TaskOffer(
            task=self.task,
            offerer=self.profile,
            status = 'a')
        self.task_offer.save()

        self.request_str = ('/projects/' + str(self.project.pk) 
            + "/tasks/" + str(self.task.id) + "/")
    
    # Task view general
    def test_task_view(self):
        request = self.factory.post(self.request_str)
        request.user = self.user
        response = task_view(request, self.project.pk, self.task.id)
        self.assertEqual(response.status_code, 200)

    # Task view 'delivery'
    def test_task_view_delivery(self):
        test_file = SimpleUploadedFile('TESTFILE.md', b"Delivered mock file", 'text/markdown')
        request = self.factory.post(self.request_str, {
                "comment": "test comment",
                "file": test_file,
                "delivery": ""
            })
        
        request.user = self.user
        response = task_view(request, self.project.pk, self.task.id)
        self.assertEqual(response.status_code, 200)
    
    # Task view 'team'
    def test_task_view_team(self):
        request = self.factory.post(self.request_str, {
                "team": ""
            })
        request.user = self.user
        response = task_view(request, self.project.pk, self.task.id)
        self.assertEqual(response.status_code, 200)
    
    # Task view 'team-add'
    def test_task_view_team_add(self):
        # Create team
        self.team = Team.objects.create(
            id=1,
            name=self.fake.name(),
            task=self.task
        )

        request = self.factory.post(self.request_str, {
                "team-id": 1,
                "team-add": ""
            })
        request.user = self.user
        response = task_view(request, self.project.pk, self.task.id)
        self.assertEqual(response.status_code, 200)
    
    # Task view 'permissions'
    def test_task_view_permissions(self):
        request = self.factory.post(self.request_str, {
                "permissions": ""
            })
        request.user = self.user
        response = task_view(request, self.project.pk, self.task.id)
        self.assertEqual(response.status_code, 200)
