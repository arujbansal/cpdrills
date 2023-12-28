from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'gender', 'codeforces_handle')


admin.site.register(UserProfile, UserProfileAdmin)
