from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from .models import UserProfile
from django.utils.functional import lazy
from django.urls import reverse


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    country = CountryField().formfield(help_text="Used only for calculating website user statistics.")
    gender = forms.ChoiceField(required=True, choices=(('Female', 'Female'), ('Male', 'Male'), ('Other', 'Other')),
                               help_text="Used only for calculating website user statistics.")
    codeforces_handle = forms.CharField(widget=forms.TextInput(attrs={'class': 'mb-3'}))
    read_terms = forms.BooleanField(required=True, initial=True,
                                    label=lazy(lambda: (
                                            "I acknowledge that I have read the <a href='%s' a>privacy policy</a>." % reverse(
                                        'privacy_policy'))))

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'username', 'country', 'gender', 'codeforces_handle', 'read_terms')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["codeforces_handle"].required = False


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].disabled = True
        self.fields["username"].disabled = True


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('codeforces_handle', 'gender', 'country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["gender"].disabled = True
        self.fields["country"].disabled = True
        self.fields["codeforces_handle"].required = False
        self.fields["gender"].help_text = "Used only for calculating website user statistics."
        self.fields["country"].help_text = "Used only for calculating website user statistics."
