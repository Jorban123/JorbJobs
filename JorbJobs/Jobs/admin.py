from django.contrib import admin
from .models import Company, Specialty, Vacansy, User, Application, Resume


class VacansyAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'specialty',
                    'company',
                    'skills',
                    'description',
                    'salary_min',
                    'salary_max',
                    'published_at',)
    readonly_fields = ('id',)


class ApplicationAmin(admin.ModelAdmin):
    list_display = ('written_username', 'written_phone', 'written_cover_letter', 'vacancy', 'user', 'is_invite', 'is_reject',)
    readonly_fields = ('id',)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'employee_count', 'owner',)
    readonly_fields = ('id',)


class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'picture',)


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user',)


admin.site.register(Company, CompanyAdmin)
admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Vacansy, VacansyAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Application, ApplicationAmin)
admin.site.register(Resume, ResumeAdmin)
