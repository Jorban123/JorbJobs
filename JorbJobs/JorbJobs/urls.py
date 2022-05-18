from Jobs.views import IndexView, VacansiesView, CompanyDetail, VacancyDetail, SpecialtyView
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Jobs.views import custom_handler404, custom_handler500

from Jobs.accounts.views import LoginUserView, RegisterUserView

from Jobs.companies.views import CompanyLetsStart, CompanyCreate, my_company

company_handling = [
    path('', my_company, name='my_company'),
    path('create/', CompanyCreate.as_view(), name='company_create'),
    path('letsstart/', CompanyLetsStart.as_view(), name='company_start'),
]
vacancies = [
        path('', VacansiesView.as_view(), name='all_vacancies'),
        path('<int:id_vacancy>', VacancyDetail.as_view(), name='vacancies_detail'),
        path('cat/<str:cat_name>', SpecialtyView.as_view(), name='vacancies_cat')
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
]

handler404 = custom_handler404
handler500 = custom_handler500

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

