from django import forms 

from . import models 

class create_assignments_form(forms.ModelForm):
    class Meta:
        model = models.assignments
        fields = ('assignment', 'description', 'categories')