from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, UpdateView

from Jobs.forms import ResumeCreateForm

from Jobs.models import Resume


class MyResumeLestStartView(LoginRequiredMixin, TemplateView):
    """Отрисовка шаблона resume_lets_start"""
    template_name = 'resume/resume_start.html'


class MyResumeView(LoginRequiredMixin, UpdateView):
    """Если резюме найдено, то переход к редактированию. Если нет, то редирект на lest_start"""
    def get(self, request, *args, **kwargs):
        resume = Resume.objects.filter(user=request.user).first()
        if resume:
            data = {
                'name': resume.name,
                'surname': resume.surname,
                'status': resume.status,
                'salary': resume.salary,
                'specialty': resume.specialty,
                'grade': resume.grade,
                'education': resume.education,
                'experience': resume.experience,
                'portfolio': resume.portfolio
            }
            form = ResumeCreateForm(initial=data)
            return render(request, 'resume/resume_edit.html', context={'form': form})
        else:
            return redirect('resume_lets_start')


class MyResumeCreateView(LoginRequiredMixin, CreateView):
    """Создание резюме"""
    template_name = 'resume/resume_create.html'
    form_class = ResumeCreateForm

    def post(self, request, *args, **kwargs):
        form = ResumeCreateForm(request.POST)
        if form.is_valid():
            resume_name = request.POST.get('name')
            resume_surname = request.POST.get('surname')
            resume_status = request.POST.get('status')
            resume_salary = request.POST.get('salary')
            resume_specialty = request.POST.get('specialty')
            resume_grade = request.POST.get('grade')
            resume_education = request.POST.get('education')
            resume_experience = request.POST.get('experience')
            resume_portfolio = request.POST.get('portfolio')
            Resume.objects.create(user=request.user,
                                  name=resume_name,
                                  surname=resume_surname,
                                  status=resume_status,
                                  salary=resume_salary,
                                  specialty=resume_specialty,
                                  grade=resume_grade,
                                  education=resume_education,
                                  experience=resume_experience,
                                  portfolio=resume_portfolio)
            return redirect('my_resume')


def resume_update(request):
    """Обновляет резюме"""
    if request.method == 'GET':
        raise Http404
    if request.method == 'POST':
        form = ResumeCreateForm(request.POST)
        if form.is_valid():
            resume_name = request.POST.get('name')
            resume_surname = request.POST.get('surname')
            resume_status = request.POST.get('status')
            resume_salary = request.POST.get('salary')
            resume_specialty = request.POST.get('specialty')
            resume_grade = request.POST.get('grade')
            resume_education = request.POST.get('education')
            resume_experience = request.POST.get('experience')
            resume_portfolio = request.POST.get('portfolio')
            Resume.objects.update(user=request.user,
                                  name=resume_name,
                                  surname=resume_surname,
                                  status=resume_status,
                                  salary=resume_salary,
                                  specialty=resume_specialty,
                                  grade=resume_grade,
                                  education=resume_education,
                                  experience=resume_experience,
                                  portfolio=resume_portfolio)
            info = 'Резюме успешно обновлено'
            return render(request, 'resume/resume_edit.html', context={'form': form,
                                                                       'info': info})


@login_required(login_url=reverse_lazy('login'))
def resume_delete(request):
    """Удаляет резюме, если оно есть. Если нет, то 404"""
    if request.method == 'GET':
        resume = Resume.objects.filter(user=request.user).first()
        if resume:
            resume.delete()
            return redirect('resume_lets_start')
        else:
            raise Http404
