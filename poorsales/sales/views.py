from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from.models import *

menu = ['About', 'Add sales', 'Contact', 'Login']


# main page for site
def index(request):
    sales = Sale.objects.all()
    return render(request, 'sales/index.html', {'sales': sales, 'menu': menu, 'title': 'Main page'})


# about page function
def about(request):
    return render(request, 'sales/about.html', {'menu': menu, 'title': 'About'})


# function responsible for places
def places(request, place):
    return HttpResponse(f'<h1>Discounts by places</h1><p>{place}</p>')

# Function for view exceptions
def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not found :(</h1>')
