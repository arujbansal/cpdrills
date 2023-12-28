from django.urls import path
from . import views

urlpatterns = [
    path('train', views.train, name='train'),
    path('train/practice/<str:topic>/<str:subcategory>', views.practice, name='practice'),
    path('train/speed', views.speed_train, name='speed_train'),
    path('ajax/update_status', views.problem_status_update, name='problem_status_update'),
]
