from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('places/<slug:place>/', places),
    path('about/', about, name='about'),
    re_path('addsale/', addsale, name='add_sales'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('sales/<slug:sale_slug>/', show_sale, name='sale'),
    path('category/<int:cat_id>/', show_category, name='category'),
]