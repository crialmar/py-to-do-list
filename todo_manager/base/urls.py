from django.urls import path

from .views import ListPending

urlpatterns = [
    path("", ListPending.as_view(), name="task"),
]
