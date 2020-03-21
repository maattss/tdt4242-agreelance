from django.test import TestCase
from projects.views import project_view, get_user_task_permissions, new_project, projects_tags, filter_tags
from projects.models import ProjectCategory, Project, Task, TaskOffer
from user.models import Profile
from faker import Faker
from factory.fuzzy import FuzzyText, FuzzyInteger
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from projects.forms import TaskOfferForm
from taggit.managers import TaggableManager
from unittest import skip
from django.http import Http404

# Boundary value test for giving task offers
class TestGiveProjectOffers(TestCase):
    def setUp(self):
        # Boundary values for number of characters in fields
        self.normal_title = FuzzyText(length=30)
        self.above_max_title = FuzzyText(length=201)
        self.below_max_title = FuzzyText(length=200)

        # Description does not specify any upper boundary
        self.normal_description = FuzzyText(length=300)

        self.above_min = FuzzyText(length=1)
        self.below_min = ""

        self.above_max_price = 1000000
        self.below_max_price = 999999
        self.normal_price = FuzzyInteger(2, 999998)
        self.above_min_price = 1
        self.below_min_price = 0
    
    def test_above_max_values(self):
        data = {
            'title': self.above_max_title.fuzz(),
            'description': self.normal_description.fuzz(),
            'price': self.above_max_price
        }
        form = TaskOfferForm(data)
        self.assertFalse(form.is_valid())

    def test_below_max_values(self):
        data = {
            'title': self.below_max_title.fuzz(),
            'description': self.normal_description.fuzz(),
            'price': self.below_max_price
        }
        form = TaskOfferForm(data)
        self.assertTrue(form.is_valid())
    
    def normal_values(self):
        data = {
            'title': self.normal_title.fuzz(),
            'description': self.normal_description.fuzz(),
            'price': self.normal_price.fuzz()
        }
        form = TaskOfferForm(data)
        self.assertTrue(form.is_valid())

    def test_above_min_values(self):
        data = {
            'title': self.above_min.fuzz(),
            'description': self.above_min.fuzz(),
            'price': self.above_min_price
        }
        form = TaskOfferForm(data)
        self.assertTrue(form.is_valid())
    
    def test_below_min_values(self):
        data = {
            'title': self.below_min,
            'description': self.below_min,
            'price': self.below_min_price
        }
        form = TaskOfferForm(data)
        self.assertFalse(form.is_valid())