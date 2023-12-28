from django.contrib import admin
from . import models as my_models

admin.site.site_header = 'CP Drills Administration'
admin.site.site_title = 'CP Drills'

admin.site.register(my_models.Problem)
admin.site.register(my_models.ProblemTopic)
admin.site.register(my_models.OnlineJudge)


class ProblemStatusAdmin(admin.ModelAdmin):
    list_display = ('userprofile', 'problem', 'solve_time', 'solve_duration')


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'problem_topic')


admin.site.register(my_models.ProblemStatus, ProblemStatusAdmin)
admin.site.register(my_models.Subcategory, SubcategoryAdmin)
