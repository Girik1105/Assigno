from django.contrib import admin
from . import models 

# Register your models here.
admin.site.register(models.forum)
admin.site.register(models.forum_member)
admin.site.register(models.forum_post)
admin.site.register(models.forum_post_comment)