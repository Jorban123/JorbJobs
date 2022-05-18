from django.contrib import admin
from .models import Company, Specialty, Vacansy, User, Application, Resume


class VacansyAdmin(admin.ModelAdmin):
    pass


class ApplicationAmin(admin.ModelAdmin):
    pass


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'location','employee_count', 'owner')
    readonly_fields = ('id',)


class SpecialtyAdmin(admin.ModelAdmin):
    pass


class UserAdmin(admin.ModelAdmin):
    pass

class ResumeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Company, CompanyAdmin)
admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Vacansy, VacansyAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Application, ApplicationAmin)
admin.site.register(Resume, ResumeAdmin)