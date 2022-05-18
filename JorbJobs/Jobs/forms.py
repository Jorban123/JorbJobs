from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import User, Company, Vacansy, Specialty
from django import forms


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='Электронная почта', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CompanyCreateForm(forms.ModelForm):
    name = forms.CharField(label='Название компании',
                           error_messages={'required': 'Введите название компании'},
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.CharField(label='География',
                               error_messages={'required': 'Введите локацию компании'},
                               widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    logo = forms.ImageField(label='Логотип', required=False,
                            error_messages={'required': 'Выберите логотип'})
    logo.widget.attrs.update({'class': 'btn btn-info'})
    logo.widget.attrs.update({'style': 'display: none'})
    description = forms.CharField(label='Информация о компании',
                                  error_messages={'required': 'Введите описание компании'},
                                  widget=forms.Textarea(attrs={'class': 'form-control'}))
    employee_count = forms.IntegerField(error_messages={'required': 'Введите количество сотрудников'})

    class Meta:
        model = Company
        fields = ('name', 'location', 'logo', 'description', 'employee_count',)


    def clean_name(self):
        name = self.cleaned_data['name']
        if not name:
            raise ValidationError('Введите название компании!')
        return name

    def clean_location(self):
        location = self.cleaned_data['location']
        if not location:
            raise  ValidationError('Введите локацию компании')
        return location

    def clean_employee_count(self):
        employee_count = self.cleaned_data['employee_count']
        if not employee_count:
            raise ValidationError('Введите количество сотрудников')
        if int(employee_count) < 1:
            raise  ValidationError('Количество сотрудников не может быть меньше одного')
        return employee_count

    def clean_description(self):
        description = self.cleaned_data['description']
        if not description:
            raise ValidationError('Введите описание компании')
        return description


class VacancyCreateForm(forms.ModelForm):
    specialty = forms.ModelChoiceField(queryset=Specialty.objects.all(), empty_label='Специальность не выбрана')

    class Meta:
        model = Vacansy
        fields = ('title', 'specialty', 'skills', 'description', 'salary_min', 'salary_max')

    def clean(self):
        salary_min = self.cleaned_data['salary_min']
        salary_max = self.cleaned_data['salary_max']
        if salary_min > salary_max:
            raise ValidationError('Минимальная зарплата не может быть больше максимальной')
