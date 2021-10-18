from django import forms 
from django.core.exceptions import ValidationError

from . import models 
from dashboard import models as dashboard_models

class create_forum_form(forms.ModelForm):
    class Meta:
        model = models.forum
        fields = ('name', 'description', 'cover')

class update_forum_form(forms.ModelForm):
    class Meta:
        model = models.forum
        fields = ('description', 'cover', 'admin')


    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        forum = kwargs.pop('forum')
        qs = models.forum.objects.get(name=forum.name)
        super(update_forum_form, self).__init__(*args, **kwargs)
        self.fields['admin'].queryset = qs.members

class create_forum_post_form(forms.ModelForm):
    class Meta:
        model = models.forum_post
        fields = ('content', 'notes', 'assignments')

    def __init__(self, user,*args, **kwargs):
        super(create_forum_post_form, self).__init__(*args, **kwargs)
        self.fields['notes'].queryset = dashboard_models.notes.objects.filter(user=user)
        self.fields['assignments'].queryset = dashboard_models.assignments.objects.filter(user=user)

    def validate_content(self, data):
        notes = data.get("notes", None)
        assignments = data.get("assignments", None)

        if notes and assignments:
            raise ValidationError("You can eiter attach an assignment or a note")
        return data