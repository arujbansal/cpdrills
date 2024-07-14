from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('privacy-policy', views.privacy_policy, name='privacy_policy'),
    path('contact-us', views.contact_us, name='contact')
]
