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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_forums"] = models.forum.objects.filter(members=self.request.user)
        return context
    

class detail_forum(LoginRequiredMixin, DetailView):
    template_name = 'forums/detail_forum.html'
    model = models.forum

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["forum_post"] = forms.create_forum_post_form(self.request.user)
        context["posts"] = models.forum_post.objects.filter(forum=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        form = forms.create_forum_post_form(user=request.user, data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.forum = self.get_object()
            form.user = self.request.user
            form.save()

            return redirect(reverse("forums:detail-forum", kwargs={
                'slug': self.get_object().slug
            }))


class update_forum(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'forums/update_forum.html'
    model = models.forum
    form_class = forms.update_forum_form

    def get_form_kwargs(self, **kwargs):
        kwargs = super(update_forum, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request":self.request,
            "forum":self.get_object(),
        })
        return kwargs

    def test_func(self):
        return self.get_object().admin == self.request.user



class join_forum(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy("forums:detail-forum",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        forum = get_object_or_404(models.forum, slug=self.kwargs.get("slug"))

        try:
            models.forum_member.objects.create(user=self.request.user, forum=forum)

        except:
            messages.warning(self.request,("Warning, already a member of {}".format(forum.name)))

        else:
            messages.success(self.request,"You are now a member of the {} forum.".format(forum.name))

        return super().get(request, *args, **kwargs)


class leave_forum(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("forums:detail-forum",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        try:
            membership = models.forum_member.objects.filter(
                user=self.request.user,
                forum__slug=self.kwargs.get("slug")
            ).get()

        except models.forum_member.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this forum because you aren't in it."
            )

        else:
            
            if membership.user == membership.forum.admin:
                messages.success(
                self.request,
                "You cannot leave the forum you are the admin!"
                )
                return super().get(request, *args, **kwargs)

            membership.delete()
            messages.success(
                self.request,
                "You have left {} forum.".format(membership.forum.name)
            )
        return super().get(request, *args, **kwargs)

