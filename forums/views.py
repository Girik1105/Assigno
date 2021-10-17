from django.shortcuts import redirect, render

from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect

from django.contrib import messages

from . import models, forms

from django.views.generic import (TemplateView,
                                  View,
                                  ListView,
                                  CreateView, 
                                  UpdateView,
                                  DetailView, 
                                  DeleteView,
                                  RedirectView) 

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.
class create_forum(LoginRequiredMixin, CreateView):
    model = models.forum
    template_name = 'forums/create_forum.html'
    form_class = forms.create_forum_form

    def post(self, request, *args, **kwargs):
        form = forms.create_forum_form(request.POST, request.FILES)

        if form.is_valid():
            form.save(commit=False)
            form.instance.admin = self.request.user
            form.save()

            return redirect(reverse('forums:list-forums'))

        else:
            form = forms.create_forum_form

class list_forum(LoginRequiredMixin, ListView):
    template_name = 'forums/list_forums.html'
    model = models.forum

class detail_forum(LoginRequiredMixin, DetailView):
    template_name = 'forums/detail_forum.html'
    model = models.forum