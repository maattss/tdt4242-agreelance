from django.test import TestCase, RequestFactory
from projects.models import Task, ProjectCategory, Project, TaskOffer, Team, TaskFile, TaskFileTeam
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
        response = task_view.task_view(request, self.project.pk, self.task.id)
        self.assertEqual(response.status_code, 200)

    # Task view 'delivery'
    def test_task_view_delivery(self):
        test_file = SimpleUploadedFile(
            self.fake.file_name(extension="md"), 
            self.fake.binary(length=64), 'text/markdown')
        request = self.factory.post(self.request_str, {
                "comment": self.fake.sentence(),
                "file": test_file,
                "delivery": ""
            })
        
        request.user = self.user
        response = task_view.task_view(request, self.project.pk, self.task.id)
        self.assertEqual(response.status_code, 200)
    
    # Task view 'team'
    def test_task_view_team(self):
        request = self.factory.post(self.request_str, {
                "team": ""
            })
        request.user = self.user
        response = task_view.task_view(request, self.project.pk, self.task.id)
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
        response = task_view.task_view(request, self.project.pk, self.task.id)
        self.assertEqual(response.status_code, 200)
    
    # Task view 'permissions'
    def test_task_view_permissions(self):
        # Add team to task
        self.team = Team.objects.create(
            id=1,
            name=self.fake.name(),
            task=self.task
        )
        # Add file to task
        test_file = SimpleUploadedFile(
            self.fake.file_name(extension="md"), 
            self.fake.binary(length=64), 'text/markdown')
        task_file = TaskFile.objects.create(task=self.task, file=test_file)
        self.task.files.add(task_file)

        # Create task file team
        TaskFileTeam.objects.create(
            file = task_file,
            team = self.team,
            name = self.fake.name()
        )
        task_file_team_string = 'permission-perobj-' + str(task_file.id) + '-' + str(self.team.id)
        request = self.factory.post(self.request_str, {
                task_file_team_string: 1,
                "permissions": ""
            })
        request.user = self.user
        response = task_view.task_view(request, self.project.pk, self.task.id)
        self.assertEqual(response.status_code, 200)
