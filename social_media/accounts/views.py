from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView

from . import forms

class SignUp(CreateView):
    # Make sure not to instantiate the class
    form_class = forms.UserCreateForm
    # Once someone has signed up successfully, revese them to the login page
    # reverse_lazy instead of just reverse to let them sign up first
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'
