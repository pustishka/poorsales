import threading

from django.contrib import admin
from django.core.mail import send_mail
from django.utils.safestring import mark_safe
from django.conf import settings
from .models import *


# multithreading for fast sending mails
def threading_for_access(self, request, queryset, modeladmin=None):
    thread = threading.Thread(target=make_access(modeladmin, request, queryset))
    thread.start()


@admin.action(description='moderated')
def make_access(modeladmin, request, queryset):
    queryset.update(access_for_post=True)
    print(queryset)
    for index in range(len(list(queryset))):
        queryset_cat = list(queryset.values('cat'))[index]['cat']
        print(queryset_cat)
        users_and_emails = dict(Profile.objects.filter(prefer_category=queryset_cat).values_list('user', 'email'))
        print(users_and_emails)
        # selecting from queryset user,email who selected prefer_category the same of adding sale
        for user, email in users_and_emails.items():
            # sending mail for each email and user with custom message
            send_mail(
                f'Привет {user}, хорошая новость!',
                f'Только что появилась новая скидка, вашей любимой категории! {list(queryset.values("title"))[index]["title"]}',
                settings.EMAIL_HOST_USER,  # take email from setting.py
                [email],
                fail_silently=False, )


class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'create_date', 'get_html_photo', 'access_for_post')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')
    actions = [threading_for_access]

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = 'Миниатюра'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Sale, SaleAdmin)
admin.site.register(Category, CategoryAdmin)
