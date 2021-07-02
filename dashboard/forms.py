from django import forms 

from django.utils import dateformat, timezone
from . import models 

from django.conf import settings

class create_assignments_form(forms.ModelForm):

    description = forms.Textarea(attrs={
        'rows':'7',
        'placeholder':'Share something with the world!',
        'class':'increase-text'
        })
    
    class Meta:
        model = models.assignments
        fields = ('title','assignment', 'description', 'categories',)

    def __init__(self, *args, **kwargs):
        usr = kwargs.pop('usr')
        categories = models.categories.objects.filter(user=usr)
        super(create_assignments_form, self).__init__(*args, **kwargs)
        self.fields['categories'].queryset = categories

class create_note_form(forms.ModelForm):
    class Meta:
        model = models.notes
        fields = ('title', 'body', 'categories')

    def __init__(self, *args, **kwargs):
        usr = kwargs.pop('usr')
        categories = models.categories.objects.filter(user=usr)
        super(create_note_form, self).__init__(*args, **kwargs)
        self.fields['categories'].queryset = categories

class create_category_form(forms.ModelForm):
    class Meta:
        model = models.categories
        fields = ('title',)

class create_deadline_form(forms.ModelForm):

    last_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)

    class Meta:
        model = models.deadlines
        fields = ('title', 'description', 'assignments', 'last_date',)
        labels = {
        "last_date": "Add a Reminder (dd/mm/yyyy) or (yyyy/mm/dd)",
        "assignments": "You can ping assignments to deadlines. (Optional)"
        }

    def __init__(self, *args, **kwargs):
        usr = kwargs.pop('usr')
        assignments = models.assignments.objects.filter(user=usr)
        super(create_deadline_form, self).__init__(*args, **kwargs)
        self.fields['assignments'].queryset = assignments