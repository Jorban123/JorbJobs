from django.db import models

from django.urls import reverse


class User(models.Model):
    name = models.CharField(max_length=64)
    password = models.CharField(max_length=16)
    email = models.EmailField()


class Company(models.Model):
    name = models.CharField(max_length=64)
    location = models.CharField(max_length=64)
    logo = models.ImageField(upload_to='MEDIA_COMPANY_IMAGE_DIR', default='https://place-hold.it/100x60')
    description = models.TextField()
    employee_count = models.IntegerField()
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('company_detail', kwargs={'pk': self.pk})


class Specialty(models.Model):
    code = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    picture = models.ImageField(upload_to='MEDIA_SPECIALITY_IMAGE_DIR', default='https://place-hold.it/100x60')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('vacancies_cat', kwargs={'cat_name': self.code})


class Vacansy(models.Model):
    title = models.CharField(max_length=64)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.TextField()
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField(auto_now=False, auto_now_add=True)

    def get_absolute_url(self):
        return reverse('vacancies_detail', kwargs={'id_vacancy': self.pk})


class User(models.Model):
    name = models.CharField(max_length=64)
    password = models.CharField(max_length=16)
    email = models.EmailField()


class Application(models.Model):
    written_username = models.CharField(max_length=64)
    written_phone = models.CharField(max_length=12)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacansy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')

