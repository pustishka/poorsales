from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import AddSaleForm
from .models import *

# All menu on main page with our urls
menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить скидки', 'url_name': 'add_sales'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Логин', 'url_name': 'login'}
        ]


# main class for main page
class SaleHome(ListView):
    model = Sale
    template_name = 'sales/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'PoorSales - Вкусные скидки для бедных!'
        context['cat_selected'] = 0
        return context


# about page function
def about(request):
    return render(request, 'sales/about.html', {'menu': menu, 'title': 'About'})


# function responsible for places
def places(request, place):
    return HttpResponse(f'<h1>Discounts by places</h1><p>{place}</p>')


# class for showing categories
class SaleCategory(ListView):
    model = Sale
    template_name = 'sales/index.html'
    context_object_name = 'sales'
    allow_empty = False

    def get_queryset(self):
        return Sale.objects.filter(cat__slug=self.kwargs['cat_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Места -" + str(context['sales'][0].cat)
        context['menu'] = menu
        context['cat_selected'] = context['sales'][0].cat_id
        return context


# class for showing each sale
class ShowSale(DetailView):
    model = Sale
    template_name = 'sales/sale.html'
    slug_url_kwarg = 'sale_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = context['sale']
        context['cat_selected'] = 0
        return context

# class for add new sales on site with save data in database
class AddSale(CreateView):
    form_class = AddSaleForm
    template_name = 'sales/addsale.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Добавление скидки'
        # context['title'] = context['sale']
        # context['cat_selected'] = 0
        return context
# def addsale(request):
#     if request.method == 'POST':
#         form = AddSaleForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddSaleForm()
#     return render(request, 'sales/addsale.html/', {'form': form, 'menu': menu, 'title': 'Добавление скидки'})


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Авторизация')


# Function for view exceptions
def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена :(</h1>')
