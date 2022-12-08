from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, UserManager, PermissionsMixin
from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField


# model for creating table comment in base
class Comment(models.Model):
    sale = models.ForeignKey('Sale', on_delete=models.CASCADE, related_name='comments', null=True)
    # after deleting sale, all includes comments was delete too
    username = models.CharField(max_length=30)
    email = models.EmailField()
    comment_body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']  # ordering for displaying the newest comments


# profile model with necessarily login
class Profile(AbstractBaseUser, PermissionsMixin):
    user = models.CharField(max_length=30, unique=True)
    email = models.CharField(max_length=255)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to='images/profile/')
    prefer_category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Приоритет мест')
    # tether prefer category with model category
    USERNAME_FIELD = 'user'
    is_staff = models.BooleanField(
        default=False)  # reassignment of the standart django user model for mixing admin and creating users
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    def __str__(self):
        return self.user


# model for feedback
class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=255)
    message = models.TextField(blank=True)

    def __str__(self):
        return self.email


# main sale model
class Sale(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', max_length=255, unique=True, db_index=True, verbose_name='URL')
    # auto slug field for correct and unique displaying on page
    normal_price = models.IntegerField()
    price_with_sale = models.IntegerField()
    sale_percent = models.IntegerField(null=True)
    place = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT,
                            verbose_name='Категории')  # field of sale model tether with category model by foreign key
    access_for_post = models.BooleanField(default=False)  # field for moderation of sales (afrer creating default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('sale', kwargs={'sale_slug': self.slug})  # adding slug in kwargs for using in views

    class Meta:
        verbose_name = 'Скидки'  # for correct displaying in admin panel
        verbose_name_plural = 'Скидки'
        ordering = ['create_date', 'title']


# model for category
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
