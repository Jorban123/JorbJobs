from django.contrib.auth.mixins import AccessMixin

from Jobs.models import Company
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from Jobs.forms import CompanyCreateForm


class PresenceCompany(AccessMixin):
    """Проверяет наличие компании, если есть, то редирект на страницу с компанией"""
    def dispatch(self, request, *args, **kwargs):
        my_company = Company.objects.filter(owner=request.user).first()
        if my_company:
            return redirect(reverse_lazy('my_company'))
        return super().dispatch(request, *args, **kwargs)


def check_company(function):
    """Декоратор, проверяющий наличие компании у пользователя.
    Если ее нет, то происходит редирект на страницу, предлагающей ее создать.
    Если она есть, то отрисовывается в шаблоне."""
    def wrap(request, *args, **kwargs):
        if not my_company:
            return redirect(reverse_lazy('company_start'))


    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
