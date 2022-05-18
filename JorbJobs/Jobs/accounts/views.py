
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView

from django.views.generic import CreateView

from Jobs.forms import RegisterUserForm


class LoginUserView(LoginView):
    """Авторизация пользователя на сайте"""
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    success_url = '/'
    template_name = 'registration/login.html'


class RegisterUserView(CreateView):
    """Регистрация пользователя на сайте"""
    form_class = RegisterUserForm
    success_url = '/'
    template_name = 'registration/register.html'

