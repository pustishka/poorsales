from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from .views import *

urlpatterns = [
    path('', cache_page(5)(SaleHome.as_view()), name='home'),  # caching main page for saving traffic and resources
    path('about/', about, name='about'),  # about page
    re_path('addsale/', AddSale.as_view(), name='add_sale'),
    re_path('contact/', ContactFormView.as_view(), name='contact'),
    re_path('login/', LoginUser.as_view(), name='login'),
    path('category/<slug:cat_slug>/', SaleCategory.as_view(), name='category'),  # display by category via slug
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('user_profile/<int:pk>/', ShowProfilePageView.as_view(), name='user_profile'),
    # display each user profile via pk
    path('sales/<slug:sale_slug>/comments', AddComment.as_view(), name='comments'),  # comment system on sales
    path('sales/<slug:sale_slug>/', ShowSale.as_view(), name='sale'),  # sales via own unique slug
    path('user_profile/<int:pk>/edit', EditProfile.as_view(), name='edit_profile')  # editing profiles via pk
]
