from django.test import TestCase
from django.contrib.auth.models import User


class UserProfileTests(TestCase):
    """
    Tests creation of a UserProfile post the creation of the respective 'User' model.
    """

    @classmethod
    def setUpTestData(cls):
        obj = User.objects.create()

    def test_profile(self):
        profile = User.objects.last().userprofile
