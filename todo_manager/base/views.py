from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Task

class ListPending(ListView):
    model = Task
    context_object_name = 'todo'