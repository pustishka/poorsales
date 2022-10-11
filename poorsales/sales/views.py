from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from .models import *

# All menu on main page with our urls
menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить скидки', 'url_name': 'add_sales'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Логин', 'url_name': 'login'}
        ]


# main page for site
def index(request):
    sales = Sale.objects.all()
    context = {
        'sales': sales,
        'menu': menu,
        'title': 'Главная страница'
    }

    return render(request, 'sales/index.html', context=context)


# about page function
def about(request):
    return render(request, 'sales/about.html', {'menu': menu, 'title': 'About'})


# function responsible for places
def places(request, place):
    return HttpResponse(f'<h1>Discounts by places</h1><p>{place}</p>')


def show_sale(request, sales_id):
    return HttpResponse(f'<h1>Скидка с id= {sales_id}')


def addsales(request):
    return HttpResponse('Добавление скидки')


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Авторизация')


# Function for view exceptions
def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена :(</h1>')
