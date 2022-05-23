import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from Jobs.forms import CompanyCreateForm, VacancyCreateForm
from Jobs.models import Company, Vacansy, Specialty, Application, User
from django.db.models import Count
from django.http import Http404

from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DetailView

from Jobs.companies.MyMixins import PresenceCompany

from JorbJobs.settings import DEFAULT_IMAGE_NAME, DEFAULT_IMAGE_DIR




class CompanyLetsStart(LoginRequiredMixin, PresenceCompany, TemplateView):
    """Показывает страницу, в которой рекомендовано создать компанию"""
    template_name = 'companies/company_lets_start.html'
    login_url = reverse_lazy('login')


@login_required(login_url=reverse_lazy('login'))
def my_company(request):
    """Отображает компанию пользователя. Если компании нет,
     то предлагается создать ее"""
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
            info = 'Информация о компании обновлена'
            return render(request, 'companies/company_update.html', context={'form': form,
                                                                             'info': info})

    return redirect(reverse('company_start'))


def delete_logo_pre_update(company):
    """Удаляет старый логотип, при выбора нового"""
    dir_name = os.path.dirname(company.logo.path)
    file_name = os.path.basename(company.logo.path)
    file_path = rf"{dir_name}\{file_name}"
    if file_name != DEFAULT_IMAGE_NAME:
        if os.path.exists(file_path):
            os.remove(file_path)


class CompanyCreate(LoginRequiredMixin, PresenceCompany, CreateView):
    """Создает компанию пользователю"""
    form_class = CompanyCreateForm
    template_name = 'companies/company_create.html'
    success_url = '/'
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        form = CompanyCreateForm(request.POST, request.FILES)
        if form.is_valid():
            company_name = request.POST.get('name')
            company_location = request.POST.get('location')
            if request.FILES.get('logo'):
                company_logo = request.FILES.get('logo')
            else:
                company_logo = DEFAULT_IMAGE_DIR
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


@login_required(login_url=reverse_lazy('login'))
def company_delete(request):
    """Позволяет удалить компанию"""
    if request.method == 'GET':
        company = Company.objects.filter(owner=request.user)
        if company:
            company.delete()
            return redirect(reverse_lazy('company_start'))
        raise Http404


class CompanyVacancies(ListView):
    """Отображает вакансии своей компании во вкладке mycompany"""
    template_name = 'companies/company_vacancies.html'

    def get(self, request, *args, **kwargs):
        vacancies = Vacansy.objects\
                                    .filter(company=request.user.company)\
                                    .select_related('specialty')\
                                    .annotate(apps=Count('applications'))
        return render(request, 'companies/company_vacancies.html', context={'vacancies': vacancies})


class CompanyVacancyCreate(CreateView):
    """Позволяет создать вакансию"""
    template_name = 'companies/company_vacancy_create.html'
    form_class = VacancyCreateForm

    def post(self, request, *args, **kwargs):
        form = VacancyCreateForm(request.POST)
        if form.is_valid():
            vacancy_title = request.POST.get('title')
            vacancy_specialty = Specialty.objects.get(id=request.POST.get('specialty'))
            vacancy_skills = request.POST.get('skills')
            vacancy_description = request.POST.get('description')
            vacancy_salary_min = request.POST.get('salary_min')
            vacancy_salary_max = request.POST.get('salary_max')
            vacancy = Vacansy.objects.create(title=vacancy_title,
                                             specialty=vacancy_specialty,
                                             skills=vacancy_skills,
                                             description=vacancy_description,
                                             salary_min=vacancy_salary_min,
                                             salary_max=vacancy_salary_max,
                                             company=request.user.company)
            vacancy.save()
            return redirect('/')
        else:
            return render(request, 'companies/company_vacancy_create.html', context={'form': form})


@login_required(login_url=reverse_lazy('login'))
def company_vacancy_update(request, pk):
    """Позволяет отредактировать инормацию о вакансии"""
    vacancy = Vacansy.objects.select_related('specialty').filter(id=pk, company__owner=request.user).first()
    if vacancy:
        if request.method == 'GET':
            data = {
                'title': vacancy.title,
                'specialty': vacancy.specialty,
                'skills': vacancy.skills,
                'description': vacancy.description,
                'salary_min': vacancy.salary_min,
                'salary_max': vacancy.salary_max
            }
            form = VacancyCreateForm(initial=data)
            return render(request, 'companies/company_vacancy_update.html', context={'form': form,
                                                                                     'pk': pk})
        if request.method == 'POST':
            form = VacancyCreateForm(request.POST)
            if form.is_valid():
                vacancy = Vacansy.objects.get(pk=pk)
                vacancy.title = request.POST.get('title')
                vacancy.specialty = Specialty.objects.get(id=request.POST.get('specialty'))
                vacancy.skills = request.POST.get('skills')
                vacancy.description = request.POST.get('description')
                vacancy.salary_min = request.POST.get('salary_min')
                vacancy.salary_max = request.POST.get('salary_max')
                vacancy.save()
                info = 'Информация о вакансии обновлена'
                return render(request, 'companies/company_vacancy_update.html', context={'form': form,
                                                                                         'pk': pk,
                                                                                         'info': info})
            return render(request, 'companies/company_vacancy_update.html', context={'form': form,
                                                                                     'pk': pk})
    else:
        raise Http404
    return render(request, 'companies/company_vacancy_update.html')


@login_required(login_url=reverse_lazy('login'))
def company_vacancy_delete(request, pk):
    """Позволяет удалить вакансию"""
    vacancy = Vacansy.objects.select_related('specialty').filter(id=pk, company__owner=request.user).first()
    if vacancy:
        vacancy.delete()
    else:
        raise Http404
    return redirect(reverse('company_vacancies'))


class VacansyApplications(ListView):
    """Просмотр откликов на вакансию"""
    template_name = 'companies/company_applications.html'
    queryset = ''
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacansyApplications, self).get_context_data()
        context['applications'] = Application.objects.filter(vacancy=self.kwargs['pk']).select_related('vacancy')
        context['vacancy'] = context['applications'].first().vacancy
        return context


class ResumeView(DetailView):
    template_name = 'companies/company_resume.html'
    context_object_name = 'user'
    pk_url_kwarg = 'pk_user'

    def get_queryset(self):
        return User.objects.filter(id=self.kwargs['pk_user']).select_related('resume')

