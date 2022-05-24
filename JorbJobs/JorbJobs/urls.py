from Jobs.views import IndexView, VacansiesView, CompanyDetail, VacancyDetail, SpecialtyView
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Jobs.views import custom_handler404, custom_handler500

from Jobs.accounts.views import LoginUserView, RegisterUserView

from Jobs.companies.views import CompanyLetsStart, CompanyCreate, CompanyVacancies, my_company, CompanyVacancyCreate,\
    company_vacancy_update, company_vacancy_delete, company_delete, VacansyApplications, ResumeView, \
    application_invite, application_reject, VacansyApplicationsInvite, VacansyApplicationsReject

from Jobs.resume.views import MyResumeView, MyResumeCreateView, resume_update, MyResumeLestStartView, resume_delete

from Jobs.application.views import application_add, MyApplications


company_handling = [
    path('', my_company, name='my_company'),
    path('create/', CompanyCreate.as_view(), name='company_create'),
    path('letsstart/', CompanyLetsStart.as_view(), name='company_start'),
    path('vacancies/', CompanyVacancies.as_view(), name='company_vacancies'),
    path('vacancies/create/', CompanyVacancyCreate.as_view(), name='company_vacancy_create'),
    path('vacancies/<int:pk>/update', company_vacancy_update, name='company_vacancy_update'),
    path('vacancies/<int:pk>/delete', company_vacancy_delete, name='company_vacancy_delete'),
    path('vacancies/<int:pk>/applications', VacansyApplications.as_view(), name='company_applications'),
    path('vacancies/<int:pk_vacancy>/resume/<int:pk_user>', ResumeView.as_view(), name='company_resume'),
    path('vacancies/<int:pk>/applications/invite', VacansyApplicationsInvite.as_view(), name='company_applications_invite'),
    path('vacancies/<int:pk>/applications/reject', VacansyApplicationsReject.as_view(), name='company_applications_reject'),
    path('application_is_invite/<int:pk>', application_invite, name='application_invite'),
    path('application_is_reject/<int:pk>', application_reject, name='application_reject'),
    path('delete/', company_delete, name='company_delete')
]
vacancies = [
        path('', VacansiesView.as_view(), name='all_vacancies'),
        path('<int:id_vacancy>', VacancyDetail.as_view(), name='vacancies_detail'),
        path('cat/<str:cat_name>', SpecialtyView.as_view(), name='vacancies_cat')
]
my_resume = [
    path('', MyResumeView.as_view(), name='my_resume'),
    path('/lets_start', MyResumeLestStartView.as_view(), name='resume_lets_start'),
    path('/create_view', MyResumeCreateView.as_view(), name='resume_create'),
    path('/update/', resume_update, name='resume_update'),
    path('/delete', resume_delete, name='resume_delete'),
]
applications = [
    path('', MyApplications.as_view(), name='my_applications')
]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='home'),
    path('signup/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('mycompany/', include(company_handling)),
    path('vacancies/', include(vacancies)),
    path('companies/<int:pk>', CompanyDetail.as_view(), name='company_detail'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('my_resume', include(my_resume)),
    path('my_applications', include(applications)),
    path('application_add/<int:pk>', application_add, name='application_add')
]

handler404 = custom_handler404
handler500 = custom_handler500

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

