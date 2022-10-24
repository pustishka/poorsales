from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', SaleHome.as_view(), name='home'),
    path('places/<slug:place>/', places),
    path('about/', about, name='about'),
    re_path('addsale/', AddSale.as_view(), name='add_sales'),
    path('contact/', contact, name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('sales/<slug:sale_slug>/', ShowSale.as_view(), name='sale'),
    path('category/<slug:cat_slug>/', SaleCategory.as_view(), name='category'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
]