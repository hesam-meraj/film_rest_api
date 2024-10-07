from django.urls import path
from .views import *
urlpatterns = [
    path('', api_home, name="api_home"),
]