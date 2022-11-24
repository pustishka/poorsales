from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, UserManager, PermissionsMixin
from django.db import models
from django.urls import reverse


class Comment(models.Model):
    sale = models.ForeignKey('Sale', on_delete=models.CASCADE, related_name='comments', null=True)
    username = models.CharField(max_length=30)
    email = models.EmailField()
    comment_body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    # def __str__(self):
    #     return f'Comment {self.comment_body} by {self.username}'
    #
    # return f'Comment {self.comment_body} by {self.username}'


class Profile(AbstractBaseUser, PermissionsMixin):
    user = models.CharField(max_length=30, unique=True)
    email = models.CharField(max_length=255)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to='images/profile/')
    prefer_category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Приоритет мест')
    USERNAME_FIELD = 'user'
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    def __str__(self):
        return self.user
    # def __str__(self):
    #     return self.user + ' ' + self.email + ' '


class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=255)
    message = models.TextField(blank=True)

    def __str__(self):
        return self.email


class Sale(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    normal_price = models.IntegerField()
    price_with_sale = models.IntegerField()
    sale_percent = models.IntegerField()
    place = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Места')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('sale', kwargs={'sale_slug': self.slug})

    class Meta:
        verbose_name = 'Скидки'
        verbose_name_plural = 'Скидки'
        ordering = ['create_date', 'title']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Места'
        verbose_name_plural = 'Места'


