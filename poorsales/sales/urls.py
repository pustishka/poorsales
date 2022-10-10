from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('places/<slug:place>/', places),
    path('about/', about, name='about'),
]