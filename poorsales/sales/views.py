from django.contrib.auth import logout, login, user_logged_in
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django import forms
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.core.mail import send_mail
from .forms import AddSaleForm, LoginUserForm, ContactForm, RegisterUserForm, AddCommentForm, ProfileFormEdit
from .models import *
from .utils import *
from django.conf import settings

# All menu on main page with our urls
menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить скидку', 'url_name': 'add_sale'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        ]


# main class for main page
class SaleHome(DataMixin, ListView):
    model = Sale
    template_name = 'sales/index.html'  # template using in view

    # getting all context for correct working title and main menu on all pages
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='PoorSales - Вкусные скидки для бедных!')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Sale.objects.filter().select_related('cat')  # reassignment queryset for displaying categories


# about page function
def about(request):
    user_menu = menu.copy()
    if not request.user.is_authenticated:  # if user not login he can't add sales in about page too
        user_menu.pop(1)
    return render(request, 'sales/about.html', {'menu': user_menu, 'title': 'О сайте'})


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
    form_class = AddCommentForm  # using django forms in view
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

    # function validate data and before saving in base delete captcha values
    def form_valid(self, form):
        del form.cleaned_data['captcha']
        form.cleaned_data['sale'] = Sale.objects.get(slug=self.kwargs["sale_slug"])
        Comment.objects.create(**form.cleaned_data)
        return redirect(f'/sales/{self.kwargs["sale_slug"]}')


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

    # function calculate automatically sale in percents and add in base
    def form_valid(self, form):
        form = form.cleaned_data
        form['sale_percent'] = 100 - (
                (form['price_with_sale'] / form['normal_price']) * 100)
        Sale.objects.create(**form)
        users_and_emails = dict(Profile.objects.filter(prefer_category=form['cat']).values_list('user', 'email'))
        # selecting from queryset user,email who selected prefer_category the same of adding sale
        for user, email in users_and_emails.items():
            # sending mail for each email and user with custom message
            send_mail(
                f'Привет {user}, хорошая новость!',
                f'Только что появилась новая скидка, вашей любимой категории! {form["title"]}',
                settings.EMAIL_HOST_USER,  # take email from setting.py
                [email],
                fail_silently=False, )
        return redirect('home')


# view for sending feedback of users
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


# view for editing user profile and update data too
class EditProfile(DataMixin, UpdateView):
    model = Profile
    form_class = ProfileFormEdit
    template_name = 'sales/edit_profile.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Редактирование')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        form.save()
        return redirect(f'/user_profile/{self.kwargs["pk"]}')  # after save data of user profile redirect on user page


# view for registration users and auto login after
class RegisterUser(DataMixin, CreateView):
    model = Profile
    form_class = RegisterUserForm
    template_name = 'sales/register.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

    success_url = reverse_lazy('home')


# view for login users
class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'sales/login.html'
    fields = ('email', 'password')  # all field what user see during login

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


# logout function and after redirect on login page
def logout_user(request):
    logout(request)
    return redirect('login')


# view for displaying profile data on page
class ShowProfilePageView(DataMixin, DetailView):
    model = Profile
    template_name = 'sales/user_profile.html'
    form_class = ProfileFormEdit

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Профиль')
        return dict(list(context.items()) + list(c_def.items()))
