from django.contrib.auth.models import User
from django.db import models
from django.forms.forms import Form
from base.resources import TaskResource
from base.models import Task
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.shortcuts import render
from django.http import HttpResponse
from tablib import Dataset
from .resources import TaskResource
from .models import Task
from django.views import View

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage,self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task # Model name
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)
        # title__icontaints=search_input for any letter search

        context['search_input'] = search_input
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title','description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate (LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title','description', 'complete']
    success_url = reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

class TaskExport(LoginRequiredMixin, View):
    model = Task
    template_name = 'base/export_data.html'
    success_url = reverse_lazy('tasks')
    context_object_name = 'tasks'

    def export_data(self, request):

        if request.method == 'POST':
            file_format = request.POST['file-format']
            task_resource = TaskResource()
            queryset = Task.objects.filter(user=self.request.user)
            dataset = task_resource.export(queryset)
            if file_format == 'CSV':
                response = HttpResponse(dataset.csv, content_type= 'text/csv')
                response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
                return response
            elif file_format == 'JSON':
                response = HttpResponse(dataset.json, content_type='application/json')
                response['Content-Disposition'] = 'attachment; filename="exported_data.json"'
                return response
            elif file_format == 'XLS (Excel)':
                response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'
                return response
            
        return render(request, self.template_name)

    def get(self, request):
       return self.export_data(request)

    def post(self, request):
       return self.export_data(request)