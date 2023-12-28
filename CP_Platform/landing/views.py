from django.shortcuts import render
from django.contrib.auth import get_user_model
from accounts.models import UserProfile

User = get_user_model()


def home(request):
    user_cnt = User.objects.all().count()
    countries_cnt = UserProfile.objects.values("country").distinct().count()
    return render(request, 'landing/index.html', {"user_cnt" : user_cnt,
                                                  "countries_cnt" : countries_cnt})


def privacy_policy(request):
    return render(request, 'landing/privacy_policy.html')


def contact_us(request):
    return render(request, 'landing/contact_us.html')
