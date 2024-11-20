from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task


class Login(LoginView):
    '''Login'''
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('pending')


class RegisterPage(FormView):
    '''Register'''
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('pending')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('pending')
        return super(RegisterPage, self).get(*args, **kwargs)


class ListPending(LoginRequiredMixin, ListView):
    '''Pending tasks'''
    model = Task
    context_object_name = 'todos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todos'] = context['todos'].filter(user=self.request.user)
        context['count'] = context['todos'].filter(complete = False)

        task_search = self.request.GET.get('search') or ''
        if task_search:
            context['todos'] = context['todos'].filter(title__icontains= task_search)
        context['task_search'] = task_search
        return context


class DetailTask(LoginRequiredMixin, DetailView):
    '''Task's detail'''
    model = Task
    context_object_name = 'todo'


class CreateTask(LoginRequiredMixin, CreateView):
    '''Task's creation'''
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('pending')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTask, self).form_valid(form)


class EditTask(LoginRequiredMixin, UpdateView):
    '''Task's edition'''
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('pending')


class DeleteTask(LoginRequiredMixin, DeleteView):
    '''Task deletion'''
    model = Task
    context_object_name = 'todo'
    success_url = reverse_lazy('pending')
