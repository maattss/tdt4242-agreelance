from django.test import TestCase
from projects.models import Task, ProjectCategory, Project, TaskOffer
from user.models import Profile, User
from faker import Faker

# Accept offer output coverage tests
class TestAcceptedTaskOffer(TestCase):
    def setUp(self):
        self.fake = Faker() # Generate fake data using a faker generator
        
        self.project_category = ProjectCategory.objects.create(pk=1)

        self.user = User.objects.create_user(
            pk=1,
            username=self.fake.user_name(),
            password=self.fake.password())

        self.profile = Profile.objects.get(user=self.user)

        self.project = Project.objects.create(
            pk=1,
            user=self.profile,
            category=self.project_category)

        self.task = Task.objects.create(project=self.project)
        self.accepted_offer = TaskOffer.objects.create(
            task=self.task,
            offerer=self.profile,
            status='a')

    # Check that accepted offer returned from accepted_task_offer is equal to task created in set up
    def test_accepted_task_offer(self):
        accepted_offer = self.task.accepted_task_offer()
        self.assertEqual(accepted_offer, self.accepted_offer)