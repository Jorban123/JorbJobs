import os

from Jobs.forms import CompanyCreateForm
from Jobs.models import Company

from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView, CreateView


class CompanyLetsStart(TemplateView):
    """Показывает страницу, в которой рекомендовано создать компанию"""

    template_name = 'companies/company_lets_start.html'


def my_company(request):
    if request.method == 'GET':
        company = Company.objects.filter(owner=request.user).first()
        if company:
            data = {
                'name': company.name,
                'location': company.location,
                'description': company.description,
                'employee_count': company.employee_count
            }
            form = CompanyCreateForm(initial=data)
            return render(request, 'companies/company_update.html', context={'form': form})

    if request.method == 'POST':
        form = CompanyCreateForm(request.POST, request.FILES)
        if form.is_valid():
            company = Company.objects.get(owner=request.user)
            company.name = request.POST.get('name')
            company.location = request.POST.get('location')
            if request.FILES.get('logo'):
                delete_logo_pre_update(company)
                company.logo = request.FILES.get('logo')
            company.description = request.POST.get('description')
            company.employee_count = request.POST.get('employee_count')
            company.save()
            return redirect(reverse('home'))
        return redirect(reverse('company_start'))


def delete_logo_pre_update(company):
    dir_name = os.path.dirname(company.logo.path)
    file_name = os.path.basename(company.logo.path)
    file_path = rf"{dir_name}\{file_name}"
    if os.path.exists(file_path):
        os.remove(file_path)


class CompanyCreate(CreateView):
    form_class = CompanyCreateForm
    template_name = 'companies/company_create.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = CompanyCreateForm(request.POST, request.FILES)
        if form.is_valid():
            company_name = request.POST.get('name')
            company_location = request.POST.get('location')
            company_logo = request.FILES.get('logo')
            company_description = request.POST.get('description')
            company_employee_count = request.POST.get('employee_count')
            company = Company.objects.create(name=company_name,
                                             location=company_location,
                                             logo=company_logo,
                                             description=company_description,
                                             employee_count=company_employee_count,
                                             owner=request.user)
            company.save()
            return redirect('/')
        else:
            return render(request, 'companies/company_create.html', context={'form': form})
