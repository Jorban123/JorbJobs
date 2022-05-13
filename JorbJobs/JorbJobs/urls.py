from Jobs.views import IndexView, VacansiesView, CompanyDetail, VacancyDetail, SpecialtyView
from django.contrib import admin
from django.urls import path, include

from JorbJobs.Jobs.views import custom_handler404, custom_handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='home'),
    path('vacancies/', include([
        path('', VacansiesView.as_view(), name='all_vacancies'),
        path('<int:id_vacancy>', VacancyDetail.as_view(), name='vacancies_detail'),
        path('cat/<str:cat_name>', SpecialtyView.as_view(), name='vacancies_cat')])
    ),
    path('companies/<int:pk>', CompanyDetail.as_view(), name='company_detail'),
    path('__debug__/', include('debug_toolbar.urls')),
]

handler404 = custom_handler404
handler500 = custom_handler500
