from django.contrib import admin
from .models import Company, Specialty, Vacansy


class VacansyAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'title',
                    'specialty',
                    'company',
                    'skills',
                    'description',
                    'salary_min',
                    'salary_max',
                    'published_at')


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'location',
                    'logo',
                    'description',
                    'employee_count')


class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'code',
                    'title',
                    'picture')


admin.site.register(Company, CompanyAdmin)
admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Vacansy, VacansyAdmin)
