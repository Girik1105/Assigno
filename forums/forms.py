from django import forms 

from . import models 

class create_forum_form(forms.ModelForm):
    class Meta:
        model = models.forum
        fields = ('name', 'description', 'cover')
