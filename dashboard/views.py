import os as os 

from django.shortcuts import render

from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, Http404

from django.conf import settings

from django.views.generic import (CreateView, 
                                  DetailView, 
                                  ListView, 
                                  UpdateView, 
                                  DeleteView,
                                  TemplateView)

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail

from . import models
from . import forms 

from django.utils import timezone

import requests
import random
# Create your views here.

@login_required
def profile_edit_view(request):
    profile = request.user.profile
    form = forms.profile_form(instance=profile)

    if request.method == 'POST':
        form = forms.profile_form(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('dashboard:home')

    context = {'form': form}
    return render(request, 'social/profile_edit.html', context)


def fetch_quote():
    endpoint = 'https://type.fit/api/quotes'

    data = requests.get(endpoint)

    if data.status_code == 200:
        data = data.json()        
        random_num = random.randint(1, 1643)

        return f"{data[random_num]['text']} ~ {data[random_num]['author']}"
    else:
        return "“Education is the most powerful weapon you can use to change the world.”"

@login_required
def home(request):

    assignments = models.assignments.objects.filter(user=request.user)
    notes = models.notes.objects.filter(user=request.user).count()
    todo = models.Task.objects.filter(user=request.user)
    deadlines = models.deadlines.objects.filter(user=request.user)

    context = {
        "recent_assignments": assignments.order_by('-timestamp')[:5],
        "assignment_count":assignments.count(),
        "notes_count":notes,
        "deadline_count":deadlines.count(),
        "deadline":deadlines.order_by('last_date')[:5],
        "todo":todo.order_by('created')[:5],
        "quote": fetch_quote(),
        "today":timezone.now()
    }

    return render(request, 'dashboard/home.html', context)



class create_assignments(LoginRequiredMixin, CreateView):
    model = models.assignments
    form_class = forms.create_assignments_form
    template_name = 'dashboard/assignments/create_assignment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['today'] = timezone.now()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect(reverse('dashboard:assignment-list'))

    def get_form_kwargs(self, **kwargs):
        kwargs = super(create_assignments, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "usr":self.request.user,
        })
        return kwargs


class update_assignments(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = models.assignments
    template_name = 'dashboard/assignments/update_assignment.html'
    form_class = forms.create_assignments_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['today'] = timezone.now()
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect(reverse('dashboard:assignment-list'))

    def test_func(self):
        assignment = self.get_object()
        return assignment.user == self.request.user

    def get_form_kwargs(self, **kwargs):
        kwargs = super(update_assignments, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "usr":self.request.user,
        })
        return kwargs

class list_assignments(LoginRequiredMixin, ListView):
    model = models.assignments
    template_name = 'dashboard/assignments/list_assignment.html'

    def get_queryset(self, *args, **kwargs):
        queryset =  super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user=self.request.user)
        # for item in queryset:
        #     print(item.categories)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['categories'] = models.categories.objects.filter(user=self.request.user)
        context['assignments_w_o_category'] = self.get_queryset(**kwargs).filter(categories=None)
        context['today'] = timezone.now()
        context['quote'] = fetch_quote()
        return context


class delete_assignment(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'dashboard/assignments/delete_assignment.html'
    model = models.assignments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['today'] = timezone.now()
        context['quote'] = fetch_quote()
        return context

    def get_success_url(self):
        return reverse_lazy('dashboard:assignment-list')

    def test_func(self):
        assignment = self.get_object()
        return assignment.user == self.request.user

class create_categories(LoginRequiredMixin, CreateView):
    model = models.categories 
    form_class = forms.create_category_form
    template_name = 'dashboard/category/create_category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['today'] = timezone.now()
        context['quote'] = fetch_quote()
        return context

    def post(self, request, *args, **kwargs):
        form = forms.create_category_form(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = self.request.user
            form.save() 
    
            return redirect(reverse("dashboard:home"))
        
        else:
            form = forms.Create_category_form

class list_categories(LoginRequiredMixin, ListView):
    model = models.categories
    template_name = 'dashboard/category/edit_category.html'

    def get_queryset(self, *args, **kwargs):
        queryset =  super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user=self.request.user)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['categories'] = self.get_queryset(**kwargs)
        context['today'] = timezone.now()
        context['quote'] = fetch_quote()
        return context

@login_required
def delete_categories(request, pk):
    try:
        category = models.categories.objects.get(user=request.user, pk=pk)
    except:
        raise Http404
    
    category.delete()

    return redirect(reverse_lazy("dashboard:category-edit"))

class create_notes(LoginRequiredMixin, CreateView):

    model = models.notes
    template_name = 'dashboard/notes/create_notes.html'
    form_class = forms.create_note_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['today'] = timezone.now()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect(reverse('dashboard:notes-list'))

    def get_form_kwargs(self, **kwargs):
        kwargs = super(create_notes, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "usr":self.request.user,
        })
        return kwargs


class detail_notes(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = models.notes
    template_name = 'dashboard/notes/detail_notes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['today'] = timezone.now()
        context['quote'] = fetch_quote()
        return context

    def test_func(self):
        notes = self.get_object()
        return notes.user == self.request.user

class list_notes(LoginRequiredMixin, ListView):

    model = models.notes
    template_name = 'dashboard/notes/list_notes.html'
    
    def get_queryset(self, *args, **kwargs):
        queryset =  super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user=self.request.user).order_by('timestamp')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['categories'] = models.categories.objects.filter(user=self.request.user)
        context['notes_w_o_category'] = self.get_queryset(**kwargs).filter(categories=None)
        context['today'] = timezone.now()
        context['quote'] = fetch_quote()
        return context

class update_notes(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = models.notes
    template_name = 'dashboard/notes/update_notes.html'
    form_class = forms.create_note_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['today'] = timezone.now()
        context['quote'] = fetch_quote()
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect(reverse('dashboard:notes-list'))

    def test_func(self):
        notes = self.get_object()
        return notes.user == self.request.user

    def get_form_kwargs(self, **kwargs):
        kwargs = super(update_notes, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "usr":self.request.user,
        })
        return kwargs

class delete_notes(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'dashboard/notes/delete_notes.html'
    model = models.notes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['today'] = timezone.now()
        return context

    def get_success_url(self):
        return reverse_lazy('dashboard:notes-list')

    def test_func(self):
        notes = self.get_object()
        return notes.user == self.request.user


class create_deadlines(LoginRequiredMixin, CreateView):
    model = models.deadlines
    template_name = 'dashboard/reminders/create_reminders.html'
    form_class = forms.create_deadline_form

    def form_valid(self, form):
        form.instance.user = self.request.user
        # print(form.instance.last_date)
        form.save()
        return redirect(reverse('dashboard:reminders-list'))

    def get_form_kwargs(self, **kwargs):
        kwargs = super(create_deadlines, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "usr":self.request.user,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['today'] = timezone.now()
        context['quote'] = fetch_quote()
        return context


class list_deadlines(LoginRequiredMixin, ListView):
    model = models.deadlines
    template_name = 'dashboard/reminders/list_reminders.html'

    def get_queryset(self, *args, **kwargs):
        queryset =  super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user=self.request.user).order_by('last_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['deadlines'] = self.get_queryset(**kwargs)
        context['today'] = timezone.now()
        context['quote'] = fetch_quote()
        return context

class update_deadlines(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = models.deadlines
    template_name = 'dashboard/reminders/update_reminders.html'
    form_class = forms.create_deadline_form

    def form_valid(self, form):
        form.instance.author = self.request.user
        # print(form.instance.last_date)
        form.save()
        return redirect(reverse('dashboard:reminders-list'))

    def test_func(self):
        deadlines= self.get_object()
        return deadlines.user == self.request.user

    def get_form_kwargs(self, **kwargs):
        kwargs = super(update_deadlines, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "usr":self.request.user,
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['today'] = timezone.now()
        context['quote'] = fetch_quote()
        return context

class delete_deadlines(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'dashboard/reminders/delete_reminders.html'
    model = models.deadlines

    def get_success_url(self):
        return reverse_lazy('dashboard:reminders-list')

    def test_func(self):
        deadlines = self.get_object()
        return deadlines.user == self.request.user


class TaskList(LoginRequiredMixin, ListView):
    model = models.Task
    template_name = 'dashboard/todo/list_todo.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user).order_by('-created').order_by('complete')
        context['count'] = context['tasks'].filter(complete=False).count()
        context['today'] = timezone.now()
        context['quote'] = fetch_quote()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        context['search_input'] = search_input
        return context
    

class TaskCreate(LoginRequiredMixin, CreateView):
    template_name = 'dashboard/todo/create_todo.html'
    success_url = reverse_lazy('dashboard:task-list')
    form_class = forms.create_todo_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now()
        context['quote'] = fetch_quote()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect(reverse_lazy('dashboard:task-list'))
    

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = models.Task
    template_name = 'dashboard/todo/update_todo.html'
    form_class = forms.update_todo_form
    success_url = reverse_lazy('dashboard:task-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect(reverse_lazy('dashboard:task-list'))

class TaskDelete(LoginRequiredMixin,  DeleteView):
    model = models.Task
    template_name = 'dashboard/todo/delete_todo.html'
    context_object_name = 'task'
    success_url = reverse_lazy('dashboard:task-list')


class meditation(TemplateView):
    template_name = "relax/index.html"