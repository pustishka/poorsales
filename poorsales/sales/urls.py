from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('places/<slug:place>/', places),
    path('about/', about, name='about'),
    path('addsales/', addsales, name='add_sales'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('sales/<int:sales_id>/', show_sale, name='sale')
]