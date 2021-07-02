from django.shortcuts import render, redirect

from django.views.generic import TemplateView

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from allauth.account.views import SignupView

class AccountSignupView(SignupView):
    def form_valid(self, form):
        if form.is_valid():
            form.save(self.request)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(self.request, user)
            return redirect('dashboard:edit-user-profile')

account_signup_view = AccountSignupView.as_view()


class index(TemplateView):
    template_name = 'landing/index.html'
