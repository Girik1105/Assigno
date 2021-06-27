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
        fields = ('title','assignment', 'description',)

class create_note_form(forms.ModelForm):
    class Meta:
        model = models.notes
        fields = ('title', 'body',)

class create_deadline_form(forms.ModelForm):

    class Meta:
        model = models.deadlines
        fields = ('title', 'description', 'assignments', 'last_date',)
        labels = {
        "last_date": "Add a Reminder (yyyy-mm-dd)"
        }