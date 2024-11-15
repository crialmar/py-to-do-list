from django.urls import path
from django.shortcuts import redirect
from django.contrib.auth import logout
from .views import ListPending, DetailTask, CreateTask, EditTask, DeleteTask, Login, RegisterPage

def custom_logout(request):
    '''Custom logout'''
    logout(request)
    return redirect('/login/')

urlpatterns = [
    path("", ListPending.as_view(), name="pending"),
    path("login/", Login.as_view(), name="login"),
    path("register/", RegisterPage.as_view(), name="register"),
    path("logout/", custom_logout, name="logout"),
    path("task/<int:pk>/", DetailTask.as_view(), name="task"),
    path("create-task/", CreateTask.as_view(), name="create-task"),
    path("edit-task/<int:pk>/", EditTask.as_view(), name="edit-task"),
    path("delete-task/<int:pk>/", DeleteTask.as_view(), name="delete-task"),
]
