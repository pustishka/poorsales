from django.contrib.auth import logout, login, user_logged_in
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django import forms
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin

from .forms import AddSaleForm, LoginUserForm, ContactForm, RegisterUserForm, AddCommentForm
from .models import *
from .utils import *

# All menu on main page with our urls
menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить скидки', 'url_name': 'add_sale'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        ]


# main class for main page
class SaleHome(DataMixin, ListView):
    model = Sale
    template_name = 'sales/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='PoorSales - Вкусные скидки для бедных!')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Sale.objects.filter().select_related('cat')


# about page function
def about(request):
    if not request.user.is_authenticated:
        user_menu = menu.copy()
        user_menu.pop(1)
    return render(request, 'sales/about.html', {'menu': user_menu, 'title': 'О сайте'})


# function responsible for places
def places(request, place):
    return HttpResponse(f'<h1>Discounts by places</h1><p>{place}</p>')


# class for showing categories
class SaleCategory(DataMixin, ListView):
    model = Sale
    template_name = 'sales/index.html'
    context_object_name = 'sales'
    allow_empty = False

    def get_queryset(self):
        return Sale.objects.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Место - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


class AddComment(LoginRequiredMixin, DataMixin, CreateView):
    template_name = 'sales/comments.html'
    form_class = AddCommentForm
    success_url = reverse_lazy('home')

    # login_url = reverse_lazy('/home')
    # raise_exception = True

    def auth(self, request):
        if not self.request.user.is_authenticated:
            logout_user()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=f'Комментарии к "{Sale.objects.get(slug=self.kwargs["sale_slug"])}"')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        del form.cleaned_data['captcha']
        form.cleaned_data['sale'] = Sale.objects.get(slug=self.kwargs["sale_slug"])
        Comment.objects.create(**form.cleaned_data)
        return redirect('home')


# class for showing each sale
class ShowSale(DataMixin, DetailView):
    model = Sale
    template_name = 'sales/sale.html'
    slug_url_kwarg = 'sale_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['sale'])
        return dict(list(context.items()) + list(c_def.items()))


# class for add new sales on site with save data in database
class AddSale(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddSaleForm
    template_name = 'sales/addsale.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('/home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление скидки')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.cleaned_data['sale_percent'] = 100 - (
                    (form.cleaned_data['price_with_sale'] / form.cleaned_data['normal_price']) * 100)
        Sale.objects.create(**form.cleaned_data)
        return redirect('home')


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'sales/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        del form.cleaned_data['captcha']
        Contact.objects.create(**form.cleaned_data)
        return redirect('home')


# Function for view exceptions
def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена :(</h1>')


class RegisterUser(DataMixin, CreateView):
    model = Profile
    form_class = RegisterUserForm
    template_name = 'sales/register.html'

    # fields = '__all__'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

    success_url = reverse_lazy('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    # model = Profile
    template_name = 'sales/login.html'
    fields = ('email', 'password')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class ShowProfilePageView(DataMixin, DetailView):
    model = Profile
    template_name = 'sales/user_profile.html'

    # slug_url_kwarg = 'sale_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Профиль')
        return dict(list(context.items()) + list(c_def.items()))
