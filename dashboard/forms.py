from django import forms 

from . import models 

class create_assignments_form(forms.ModelForm):

    description = forms.Textarea(attrs={
        'rows':'7',
        'placeholder':'Share something with the world!',
        'class':'increase-text'
        })
    
    class Meta:
        model = models.assignments
        fields = ('title','assignment', 'description', 'categories')