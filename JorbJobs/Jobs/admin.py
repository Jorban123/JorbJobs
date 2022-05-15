from django.contrib import admin
from .models import Company, Specialty, Vacansy, User, Application, Resume


class VacansyAdmin(admin.ModelAdmin):
    pass


class ApplicationAmin(admin.ModelAdmin):
    pass


class CompanyAdmin(admin.ModelAdmin):
    pass


class SpecialtyAdmin(admin.ModelAdmin):
    pass


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('id', 'name', 'password', 'email', )

class ResumeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Company, CompanyAdmin)
admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Vacansy, VacansyAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Application, ApplicationAmin)
admin.site.register(Resume, ResumeAdmin)