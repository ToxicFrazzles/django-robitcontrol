from django.urls import path, register_converter
from . import views

app_name = "robitcontrol"

urlpatterns = [
    path('', views.Index.as_view(), name='index')
]
