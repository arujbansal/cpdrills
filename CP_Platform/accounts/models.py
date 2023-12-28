from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User

GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))


class UserProfile(models.Model):
    """
    Extended user profile.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = CountryField()
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    codeforces_handle = models.CharField(max_length=255, blank=True)
    read_terms = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
