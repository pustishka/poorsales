from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect

from .forms import AddSaleForm
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
        'title': 'Главная страница',
    }

    return render(request, 'sales/index.html', context=context)


# about page function
def about(request):
    return render(request, 'sales/about.html', {'menu': menu, 'title': 'About'})


# function responsible for places
def places(request, place):
    return HttpResponse(f'<h1>Discounts by places</h1><p>{place}</p>')


def show_category(request, cat_id):
    sales = Sale.objects.filter(cat_id=cat_id)

    context = {
        'sales': sales,
        'menu': menu,
        'title': 'Отображение по местам',
        'cat_selected': cat_id,
    }

    return render(request, 'sales/index.html', context=context)


def show_sale(request, sale_slug):
    sale = get_object_or_404(Sale, slug=sale_slug)

    context = {
        'sale': sale,
        'menu': menu,
        'title': sale.title,
        'cat_selected': sale.cat_id,
    }

    return render(request, 'sales/sale.html', context=context)

# Function for add new sales on site with save data in database
def addsale(request):
    if request.method == 'POST':
        form = AddSaleForm(request.POST, request.FILES)
        if form.is_valid():
            # print(form.cleaned_data)
                form.save()
                return redirect('home')
    else:
        form = AddSaleForm()
    return render(request, 'sales/addsale.html/', {'form': form, 'menu': menu, 'title': 'Добавление скидки'})


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Авторизация')


# Function for view exceptions
def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена :(</h1>')
