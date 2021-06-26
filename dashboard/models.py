from django.db import models

from ckeditor.fields import RichTextField

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class user_profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length = 150, blank = True, null = True)

    profile_picture = models.ImageField(upload_to='uploads/profile_pictures', default='uploads/profile_pictures/default.png', blank=True)
    background = models.ImageField(upload_to='uploads/profile_background', default='uploads/profile_background/default.jpg', blank=True)

    GENDER_CHOICES = (
        ('', 'Choose Your Gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Rather Not Say', 'Rather Not Say')
    )

    gender = models.CharField(max_length=14, choices=GENDER_CHOICES)
    birth_date = models.DateField(blank = True, null = True)
    location = models.CharField(max_length = 150, blank = True, null = True)

    def __str__(self):
        return self.user.username

class categories(models.Model):
    title = models.CharField(max_length = 100)

    def __str__(self):
        return self.title

class assignments(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    assignment = models.FileField(upload_to='uploads/student_assignments', blank=True, null=True) # REMEMBER TO REMOVE BLANK AND NULL
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    categories = models.ManyToManyField(categories, related_name="assignment_in_category",blank=True)

    def __str__(self):
        return self.user.usernametitle

class notes(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    body = RichTextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    categories = models.ManyToManyField(categories,related_name="notes_in_category",blank=True)

    def __str__(self):
        return self.user.username

class deadlines(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    assignments = models.ForeignKey(assignments, blank=True, null=True, on_delete = models.CASCADE)
    
    last_date = models.DateField()

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
