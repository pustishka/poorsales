from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
from .models import *


class ProfileFormEdit(forms.ModelForm):
    change_category = forms.ModelChoiceField(label='Любимые места', widget=forms.Select,
                                             queryset=Category.objects.all())

    class Meta:
        model = Profile
        fields = ('change_category',)

class AddCommentForm(forms.ModelForm):
    username = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    comment_body = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 7}))
    captcha = CaptchaField(label="Код")

    class Meta:
        model = Comment
        fields = ('username', 'comment_body')


class AddSaleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Не выбрано'

    title = forms.CharField(label='Название', widget=forms.TextInput(attrs={'class': 'form-input'}))
    normal_price = forms.IntegerField(label='Обычная цена', widget=forms.TextInput(attrs={'size': 11}))
    price_with_sale = forms.IntegerField(label='Скидочная цена', widget=forms.TextInput(attrs={'size': 11}))
    place = forms.CharField(label='Место', widget=forms.TextInput(attrs={'class': 'form-input'}))
    description = forms.CharField(label='Описание', widget=forms.Textarea(attrs={'class': 'form-input'}))
    duration = forms.IntegerField(label='Длительность', widget=forms.TextInput(attrs={'size': 11}))
    photo = forms.ImageField(label='Изображение')

    class Meta:
        model = Sale
        fields = ('title', 'place', 'description', 'photo', 'cat', 'normal_price', 'price_with_sale', 'duration')

        widgets = {
            'title': forms.Textarea(attrs={'class': 'form-input', 'rows': 1}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }

    def clear_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')

        return title


class RegisterUserForm(UserCreationForm):
    user = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-input'}))
    bio = forms.CharField(label='О себе', widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 7}))
    prefer_category = forms.ModelChoiceField(label='Любимые места', widget=forms.Select,
                                             queryset=Category.objects.all())
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    avatar = forms.ImageField(label='Аватар')

    class Meta:
        model = Profile
        fields = ('user', 'email', 'bio', 'avatar', 'prefer_category', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    message = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField(label="Код")

    class Meta:
        model = Contact
        fields = ('name', 'email', 'message')
