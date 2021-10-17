from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from django.utils.text import slugify

from dashboard import models as dashboard_models
# Create your models here.

class forum(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    admin = models.ForeignKey(User, blank=True, related_name='forum_admin', on_delete= models.CASCADE)

    members = models.ManyToManyField(User, through='forum_member')
    cover = models.ImageField(upload_to='uploads/covers', default='uploads/covers/default.jpg', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    slug = models.SlugField(allow_unicode=True, unique=True)

    def __str__(self):
        return self.name

    class Meta():
        ordering = ["-timestamp"]


class forum_member(models.Model):
    forum = models.ForeignKey(forum, related_name='user_forums', on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name='memberships', on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    class Meta():
        unique_together = ('user', 'forum')


@receiver(pre_save, sender=forum)
def forum_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
    
@receiver(post_save, sender=forum)
def forum_save_member(sender, instance, created, *args, **kwargs):
    if not forum_member.objects.filter(user=instance.admin, forum=instance).exists():
        forum_member.objects.create(user=instance.admin, forum=instance)


class forum_post(models.Model):
    forum = models.ForeignKey(forum, related_name='forum', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField()
    notes = models.ForeignKey(dashboard_models.notes, related_name='note_shared_on', on_delete=models.CASCADE)
    assignments =  models.ForeignKey(dashboard_models.assignments, related_name='assignment_shared_on', on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now_add=True)

    
class forum_post_comment(models.Model):
    forum_post = models.ForeignKey(forum_post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField()

    timestamp = models.DateTimeField(auto_now_add=True)