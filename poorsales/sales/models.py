from django.db import models
from django.urls import reverse


class Sale(models.Model):
    title = models.CharField(max_length=255)
    normal_price = models.IntegerField()
    price_with_sale = models.IntegerField()
    sale_percent = models.IntegerField()
    place = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('sale', kwargs={'sales_id': self.pk})
