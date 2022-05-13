from django.db.models import Count
from django.views.generic import ListView, DetailView
from .models import Vacansy, Specialty, Company


class IndexView(ListView):
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
    model = Vacansy
    template_name = 'vacancies.html'
    context_object_name = 'vacansies'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacansiesView, self).get_context_data()
        context['title'] = 'Все вакансии'
        context['amount'] = Vacansy.objects.aggregate(amount=Count('id'))['amount']
        return context

    def get_queryset(self):
        return Vacansy.objects \
                        .select_related('company') \
                        .select_related('specialty')


class CompanyDetail(ListView):
    template_name = 'company.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        return Vacansy.objects \
            .select_related('company') \
            .select_related('specialty')\
            .filter(company__id=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CompanyDetail, self).get_context_data()
        comp = Company.objects.get(id=self.kwargs['pk'])
        context['company_title'] = comp.name
        context['city'] = comp.location
        context['amount_vacansy'] = Vacansy.objects \
            .select_related('company') \
            .filter(company__id=self.kwargs['pk']) \
            .aggregate(amount=Count('id'))['amount']
        return context


class VacancyDetail(DetailView):
    model = Vacansy
    template_name = 'vacancy.html'
    context_object_name = 'vacansy'
    pk_url_kwarg = 'id_vacancy'


class SpecialtyView(ListView):
    template_name = 'vacancies.html'
    context_object_name = 'vacansies'

    def get_queryset(self):
        return Vacansy.objects\
            .select_related('company')\
            .select_related('specialty')\
            .filter(specialty__code=self.kwargs['cat_name'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SpecialtyView, self).get_context_data()
        title = Specialty.objects.filter(code=self.kwargs['cat_name'])[0]
        context['title'] = title.title
        return context
