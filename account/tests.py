from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from account.models import Account



class CustomUserTestCase(TestCase):

    def test_main_create_user(self):
        user = Account.objects.create_user("test@test.com","tester" ,"1900-09-09","123 road","testPass123")
        self.assertTrue(isinstance(user, Account))

    def test_invalid_date_create_user(self):
        user = Account.objects.create_user("test@test.com","tester" ,"1909-01-01","123 road","password")
        self.assertFalse(isinstance(user, Account))