from django.db import models
from django.db.models import CharField, ForeignKey, TextField,\
    IntegerField, DateField, URLField
from django.urls import reverse


class Company(models.Model):
    name = CharField(max_length=64)
    location = CharField(max_length=64)
    logo = URLField(default='https://place-hold.it/100x60')
    description = TextField()
    employee_count = IntegerField()

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('company_detail', kwargs={'pk': self.pk})

class Specialty(models.Model):
    code = CharField(max_length=64)
    title = CharField(max_length=64)
    picture = URLField(default='https://place-hold.it/100x60')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('vacancies_cat', kwargs={'cat_name': self.code})

class Vacansy(models.Model):
    title = CharField(max_length=64)
    specialty = ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = TextField()
    description = TextField()
    salary_min = IntegerField()
    salary_max = IntegerField()
    published_at = DateField(auto_now=False, auto_now_add=True)

    def get_absolute_url(self):
        return reverse('vacancies_detail', kwargs={'id_vacancy': self.pk})
