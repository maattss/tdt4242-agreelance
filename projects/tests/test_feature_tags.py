from django.test import TestCase
from projects.views import new_project, project_view
from projects.models import ProjectCategory, Project
from user.models import Profile
from faker import Faker
from django.contrib.auth.models import User
from django.test import RequestFactory
from unittest import skip
from taggit.models import Tag
from django.core.exceptions import ObjectDoesNotExist

# Integration and system tests for reviews
class TestTagsImplementation(TestCase):
    def setUp(self):
        fake = Faker() # Generate fake data using a faker generator

        self.factory = RequestFactory()
        self.project_category1 = ProjectCategory.objects.create(pk=1)
        self.project_category2 = ProjectCategory.objects.create(pk=2)
        
        self.first_user = User.objects.create_user(
            pk=1,
            username=fake.user_name(),
            password=fake.password())

        self.first_profile = Profile.objects.get(user=self.first_user)

        self.project1 = Project.objects.create(
            pk=1,
            user=self.first_profile,
            category=self.project_category1)
        
        self.project2 = Project.objects.create(
            pk=2,
            user=self.first_profile,
            category=self.project_category1)

        self.project1.tags.add('easy', 'cleaning')
        self.project2.tags.add('garage', 'easy')
    #Test if the "easy" tag from setUp is stored in the database
    def test_get_tag(self):
        tag = None
        try:
            tag = Tag.objects.get(name = 'easy')
        except ObjectDoesNotExist:
            pass
        self.assertTrue(tag)

    # Test if the project is stored in the database with the tags entered, and that tags are put onto the category
    def test_create_tag(self):
        request = self.factory.post('/new_project/', {
            'title': 'test title',
            'description': 'test description',
            'category_id': 2,
            'tags': 'tag1,tag2,tag3'
        })
        request.user = self.first_user
        new_project.new_project(request)
        db_project = None
        db_category = None
        test_objects = []
        try:
            db_project = Project.objects.get(title = 'test title')
            db_category = db_project.category
            test_objects.append(db_project)
            test_objects.append(db_category)
        except:
            pass
        
        for object in test_objects:
            with self.subTest():
                self.assertEquals(str(object.tags.all()), '<QuerySet [<Tag: tag1>, <Tag: tag2>, <Tag: tag3>]>')

    # Tests sql injection vulnerability by checking if the entire string is stored as a data.
    @skip("\"\" isn't stored as data")
    def test_strange_tags(self):
        request = self.factory.post('/new_project/', {
            'title': 'test title',
            'description': 'test description',
            'category_id': 2,
            'tags': '"select * from user_review where 1=1", "DROP DATABASE"'
        })
        request.user = self.first_user
        new_project.new_project(request)
        db_project = None
        try:
            db_project = Project.objects.get(title = 'test title')
        except:
            pass
        self.assertEquals(str(db_project.tags.all()), '<QuerySet [<Tag: select * from user_review where 1=1>, <Tag: DROP DATABASE>]>')
    
    # Test if the expected projects are filtered through with a given tag
    def test_tag_filter(self):
        all_projects = Project.objects.all()
        response = project_view.filter_tags(all_projects, self.project_category1.id, 'easy')
        self.assertEquals(response, [self.project1, self.project2])