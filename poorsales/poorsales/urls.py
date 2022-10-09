from django.contrib import admin
from django.urls import path

from sales.views import *
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sales/', include('sales.urls')),

]
