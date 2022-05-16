from django.views.generic import DetailView, TemplateView


class CompanyLetsStart(TemplateView):
    template_name = 'companies/company-create.html'

class CompanyCreate():
    pass