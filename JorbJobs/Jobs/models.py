import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse
from PIL import Image

from JorbJobs.settings import MEDIA_COMPANY_IMAGE_DIR, MEDIA_SPECIALITY_IMAGE_DIR, DEFAULT_IMAGE_NAME


class User(AbstractUser):
    pass


class Company(models.Model):
    name = models.CharField(max_length=64)
    location = models.CharField(max_length=64)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR, default='https://place-hold.it/100x60')
    description = models.TextField()
    employee_count = models.PositiveIntegerField()
    owner = models.OneToOneField('User', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(Company, self).save(*args, **kwargs)
        img = Image.open(self.logo.path)
        img = img.resize((500, 500))
        img.save(self.logo.path)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('company_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


@receiver(post_delete, sender=Company)
def delete_profile(sender, instance, *args, **kwargs):
    if instance.logo.path:
        dir_name = os.path.dirname(instance.logo.path)
        file_name = os.path.basename(instance.logo.path)
        file_path = rf"{dir_name}\{file_name}"
        if file_name != DEFAULT_IMAGE_NAME:
            if os.path.exists(file_path):
                os.remove(file_path)
    print("Логотип удален")


class Specialty(models.Model):
    code = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR, default='https://place-hold.it/100x60')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('vacancies_cat', kwargs={'cat_name': self.code})

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'


class Vacansy(models.Model):
    title = models.CharField(max_length=64)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.TextField()
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('vacancies_detail', kwargs={'id_vacancy': self.pk})

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'


class Application(models.Model):
    written_username = models.CharField(max_length=64)
    written_phone = models.CharField(max_length=12)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacansy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    is_invite = models.BooleanField(null=True)
    is_reject = models.BooleanField(null=True)

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'


class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resume')
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)

    class WorkStatusChoices(models.TextChoices):
        not_in_search = 'Не ищу работу'
        consideration = 'Рассматриваю предложения'
        in_search = 'Ищу работу'

    status = models.CharField(max_length=100,
                              choices=WorkStatusChoices.choices,
                              default=WorkStatusChoices.in_search)
    salary = models.CharField(max_length=15)

    class SpecialtyChoices(models.TextChoices):
        frontend = 'Фронтенд'
        backend = 'Бэкенд'
        gamedev = 'Геймдев'
        devops = 'Девопс'
        design = 'Дизайн'
        products = 'Продукты'
        management = 'Менеджмент'
        testing = 'Тестирование'

    specialty = models.CharField(max_length=64,
                                 choices=SpecialtyChoices.choices,
                                 default=SpecialtyChoices.frontend)

    class GradeChoices(models.TextChoices):
        intern = 'intern'
        junior = 'junior'
        middle = 'middle'
        senior = 'senior'
        lead = 'lead'

    grade = models.CharField(max_length=100,
                             choices=GradeChoices.choices,
                             default=GradeChoices.intern)

    class EducationChoices(models.TextChoices):
        missing = 'Отсутствует'
        secondary = 'Среднее'
        vocational = 'Средне-специальное'
        incomplete_higher = 'Неполное высшее'
        higher = 'Высшее'

    education = models.CharField(max_length=100, choices=EducationChoices.choices)
    experience = models.CharField(max_length=100)
    portfolio = models.URLField()

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'
