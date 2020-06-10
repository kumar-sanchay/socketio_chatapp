from django.shortcuts import render, reverse
from .forms import LoginForm
from django.views.generic import FormView, View
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin


class Login(FormView):
    form_class = LoginForm
    template_name = 'login.html'

    def form_valid(self, form):
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password'])
        if user is not None:
            login(self.request, user)
        else:
            return super(Login, self).form_invalid(form)
        return super(Login, self).form_valid(form)

    def form_invalid(self, form):
        pass

    def get_success_url(self):
        return reverse('chat:dashboard')