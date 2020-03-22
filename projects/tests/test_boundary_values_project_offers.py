from django.test import TestCase
from factory.fuzzy import FuzzyText, FuzzyInteger
from projects.forms import TaskOfferForm
import copy

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
        valid_data = get_valid_data(self)
        for item in data.items():
            if(item[0] == "description"): # No max limit for description
                continue
            valid_data_copy = copy.copy(valid_data)
            valid_data_copy[item[0]] = item[1]
            form = TaskOfferForm(valid_data_copy)
            with self.subTest(form=form):
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
        data = get_valid_data(self)
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
        valid_data = get_valid_data(self)
        for item in data.items():
            valid_data_copy = copy.copy(valid_data)
            valid_data_copy[item[0]] = item[1]
            form = TaskOfferForm(valid_data_copy)
            with self.subTest(form=form):
                self.assertFalse(form.is_valid())

def get_valid_data(self):
    return {
        'title': self.normal_title.fuzz(),
        'description': self.normal_description.fuzz(),
        'price': self.normal_price.fuzz()
    }