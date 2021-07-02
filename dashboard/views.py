from django.contrib.auth import login
from django.db.models import query
from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse, request

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

    assignments = models.assignments.objects.filter(user=request.user)
    notes = models.notes.objects.filter(user=request.user).count()
    deadlines = models.deadlines.objects.filter(user=request.user)

    context = {
        "recent_assignments": assignments.order_by('-timestamp')[:3],
        "assignment_count":assignments.count(),
        "notes_count":notes,
        "deadline_count":deadlines.count(),
        "deadline":deadlines.order_by('last_date')[:3],
    }

    return render(request, 'dashboard/home.html', context)



class create_assignments(LoginRequiredMixin, CreateView):
    model = models.assignments
    form_class = forms.create_assignments_form
    template_name = 'dashboard/create_assignment.html'

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
    template_name = 'dashboard/create_assignment.html'
    form_class = forms.create_assignments_form

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
    template_name = 'dashboard/list_assignment.html'

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
        return context


class delete_assignment(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'dashboard/assignment_delete.html'
    model = models.assignments

    def get_success_url(self):
        return reverse_lazy('dashboard:assignment-list')

    def test_func(self):
        assignment = self.get_object()
        return assignment.user == self.request.user

class create_categories(LoginRequiredMixin, CreateView):
    model = models.categories 
    form_class = forms.create_category_form
    template_name = 'dashboard/create_category.html'

    def post(self, request, *args, **kwargs):
        form = forms.create_category_form(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = self.request.user
            form.save() 
    
            return redirect(reverse("dashboard:home"))
        
        else:
            form = forms.Create_category_form

class delete_categories(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'dashboard/category_delete.html'
    model = models.categories

    def get_success_url(self):
        return reverse_lazy('dashboard:assignment-list')

    def test_func(self):
        category = self.get_object()
        return category.user == self.request.user


class create_notes(LoginRequiredMixin, CreateView):

    model = models.notes
    template_name = 'dashboard/create_notes.html'
    form_class = forms.create_note_form

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
    template_name = 'dashboard/detail_notes.html'

    def test_func(self):
        notes = self.get_object()
        return notes.user == self.request.user

class list_notes(LoginRequiredMixin, ListView):

    model = models.notes
    template_name = 'dashboard/list_notes.html'
    
    def get_queryset(self, *args, **kwargs):
        queryset =  super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['categories'] = models.categories.objects.filter(user=self.request.user)
        context['notes_w_o_category'] = self.get_queryset(**kwargs).filter(categories=None)
        return context

class update_notes(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = models.notes
    template_name = 'dashboard/create_notes.html'
    form_class = forms.create_note_form

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
    template_name = 'dashboard/notes_delete.html'
    model = models.notes

    def get_success_url(self):
        return reverse_lazy('dashboard:notes-list')

    def test_func(self):
        notes = self.get_object()
        return notes.user == self.request.user


class create_deadlines(LoginRequiredMixin, CreateView):
    model = models.deadlines
    template_name = 'dashboard/create_deadlines.html'
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


class list_deadlines(LoginRequiredMixin, ListView):
    model = models.deadlines
    template_name = 'dashboard/list_deadlines.html'


    def get_queryset(self, *args, **kwargs):
        queryset =  super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user=self.request.user).order_by('last_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['deadlines'] = self.get_queryset(**kwargs)
        return context

class update_deadlines(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = models.deadlines
    template_name = 'dashboard/create_deadlines.html'
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

class delete_deadlines(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'dashboard/delete_deadlines.html'
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
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        context['search_input'] = search_input
        return context


class TaskCreate(LoginRequiredMixin, CreateView):
    model = models.Task
    template_name = 'dashboard/todo/create_todo.html'
    fields = ['title', 'description', ]
    success_url = reverse_lazy('dashboard:task-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = models.Task
    template_name = 'dashboard/todo/update_todo.html'
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('dashboard:task-list')


class TaskDelete(LoginRequiredMixin,  DeleteView):
    model = models.Task
    template_name = 'dashboard/todo/delete_todo.html'
    context_object_name = 'task'
    success_url = reverse_lazy('dashboard:task-list')