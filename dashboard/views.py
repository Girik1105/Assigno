from django.db.models import query
from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse

from django.views.generic import (CreateView, 
                                  DetailView, 
                                  ListView, 
                                  UpdateView, 
                                  DeleteView)

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from . import models
from . import forms 

# Create your views here.

@login_required
def home(request):

    assignments = models.assignments.objects.filter(user=request.user).count()
    notes = models.notes.objects.filter(user=request.user).count()
    deadlines = models.deadlines.objects.filter(user=request.user).count()

    context = {
        "assignment_count":assignments,
        "notes_count":notes,
        "deadline_count":deadlines,
    }

    return render(request, 'dashboard/home.html', context)



class create_assignments(LoginRequiredMixin, CreateView):
    model = models.assignments
    form_class = forms.create_assignments_form
    template_name = 'dashboard/create_assignment.html'

    def post(self, request, *args, **kwargs):
        form = forms.create_assignments_form(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = self.request.user
            form.save() 
    
            return redirect(reverse("dashboard:home"))
        
        else:
            form = forms.Create_assignments_form


class list_assignments(LoginRequiredMixin, ListView):
    template_name = 'dashboard/assignment_list.html'
    model = models.assignments
    template_name = 'dashboard/list_assignment.html'

    def get_queryset(self, *args, **kwargs):
        queryset =  super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['assignments'] = self.get_queryset(**kwargs)
        return context