from Jobs.forms import ApplicationForm
from Jobs.models import Application, Vacansy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy


@login_required(login_url=reverse_lazy('login'))
def application_add(request, pk):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            candidate_name = request.POST.get('written_username')
            candidate_phone = request.POST.get('written_phone')
            candidate_message = request.POST.get('written_cover_letter')
            Application.objects.create(written_username=candidate_name,
                                       written_phone=candidate_phone,
                                       written_cover_letter=candidate_message,
                                       vacancy=Vacansy.objects.get(pk=pk),
                                       user=request.user)
            messages.success(request, 'Отклик успешно отправлен')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        raise Http404
