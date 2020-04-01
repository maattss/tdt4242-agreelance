from django.test import TestCase
from projects.views import task_view
from projects.models import ProjectCategory, Project, Task, TaskOffer
from user.models import Profile
from faker import Faker
from django.contrib.auth.models import User

# Full statement coverage test of the get_user_task_permission() function
class TestGetUserTaskPermissions(TestCase):
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
        
        self.first_profile = Profile.objects.get(user=self.first_user)
        self.second_profile = Profile.objects.get(user=self.second_user)
        
        self.project = Project.objects.create(
            pk=1,
            user=self.first_profile,
            category=self.project_category)
        
        self.first_task = Task.objects.create(project=self.project)
        self.second_task = Task.objects.create(project=self.project)

        self.task_offer = TaskOffer.objects.create(
            task=self.second_task,
            offerer=self.second_profile,
            status='a')

    # Test owner permissions - All permissions
    def test_user_owner(self):
        self.assertEquals(task_view.get_user_task_permissions(self.first_user, self.first_task),
            {
                'write': True,
                'read': True,
                'modify': True,
                'owner': True,
                'upload': True,
            })

    # Test accepted offer permissions - Some permissions
    def test_user_accepted(self):
        self.assertEquals(task_view.get_user_task_permissions(self.second_user, self.second_task),
            {
                'write': True,
                'read': True,
                'modify': True,
                'owner': False,
                'upload': True,
            })

    # Test regular user permissions - No permissions
    def test_no_owner(self):
        self.assertEquals(task_view.get_user_task_permissions(self.second_user, self.first_task),
            {
                'write': False,
                'read': False,
                'modify': False,
                'owner': False,
                'view_task': False,
                'upload': False,
            })
