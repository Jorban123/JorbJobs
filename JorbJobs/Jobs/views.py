from django.db.models import Count
from django.http import HttpResponseNotFound
from django.http import HttpResponseServerError
from django.views.generic import ListView, DetailView, CreateView

from .forms import ApplicationForm
from .models import Vacansy, Specialty, Company


class IndexView(ListView):
    """Генерирует начальную страницу сайта"""
    model = Specialty
    template_name = 'index.html'
    context_object_name = 'specialties'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['companies'] = Company.objects.annotate(vacansies_count=Count('vacancies'))
        return context

    def get_queryset(self):
        return Specialty.objects.annotate(vacansies_count=Count('vacancies'))


class VacansiesView(ListView):
    """Генерирует все вакансии"""
    model = Vacansy
    template_name = 'vacancies.html'
    context_object_name = 'vacansies'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacansiesView, self).get_context_data()
        context['title'] = 'Все вакансии'
        context['amount'] = Vacansy.objects.aggregate(amount=Count('id'))['amount']
        context['applications'] = Vacansy.objects.filter(applications__user=self.request.user)
        return context

    def get_queryset(self):
        return Vacansy.objects \
                        .select_related('company') \
                        .select_related('specialty')


class CompanyDetail(ListView):
    """Генерирует все вакансии конкретной компании"""
    model = Vacansy
    template_name = 'company.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        return Vacansy.objects \
            .select_related('company')\
            .filter(company=self.kwargs['pk'])\
            .select_related('specialty')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CompanyDetail, self).get_context_data()
        company = Company.objects.get(id=self.kwargs['pk'])
        context['company_title'] = company.name
        context['location'] = company.location
        context['logo'] = company.logo.url
        context['amount'] = Vacansy.objects.filter(company__pk=self.kwargs['pk']).aggregate(amount=Count('id'))['amount']
        context['applications'] = Vacansy.objects.filter(applications__user=self.request.user)
        return context


class VacancyDetail(DetailView, CreateView):
    """Генерирует детальную информацию по конкретной вакансии"""
    form_class = ApplicationForm
    model = Vacansy
    template_name = 'vacancy.html'
    context_object_name = 'vacansy'
    pk_url_kwarg = 'id_vacancy'

    def get_queryset(self):
        return Vacansy.objects.select_related('specialty')\
                              .select_related('company')
    def get_context_data(self, **kwargs):
        context = super(VacancyDetail, self).get_context_data()
        context['applications'] = Vacansy.objects.filter(applications__user=self.request.user)
        return context


class SpecialtyView(ListView):
    """Генерирует вакансии по конкретной специальности"""
    template_name = 'vacancies.html'
    context_object_name = 'vacansies'

    def get_queryset(self):
        return Vacansy.objects\
            .select_related('company')\
            .select_related('specialty')\
            .filter(specialty__code=self.kwargs['cat_name'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SpecialtyView, self).get_context_data()
        title = Specialty.objects.get(code=self.kwargs['cat_name'])
        context['title'] = title.title
        context['amount'] = Vacansy.objects.select_related('specialty')\
                                           .filter(specialty__code=self.kwargs['cat_name'])\
                                           .aggregate(amount=Count('id'))['amount']
        context['applications'] = Vacansy.objects.filter(applications__user=self.request.user)
        return context


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ой, что то сломалось... Простите извините!')


def custom_handler500(request):
    return HttpResponseServerError()
