from django.contrib import admin

from . import models 

# Register your models here.
admin.site.register(models.user_profile)
admin.site.register(models.categories)
admin.site.register(models.assignments)
admin.site.register(models.notes)
admin.site.register(models.deadlines)
admin.site.register(models.Task)