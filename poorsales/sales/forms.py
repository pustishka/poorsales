from django import forms
from .models import *

class AddSaleForm(forms.Form):
    title = forms.CharField(max_length=255)
    slug = forms.SlugField(max_length=255)
    normal_price = forms.IntegerField()
    price_with_sale = forms.IntegerField()
    sale_percent = forms.IntegerField()
    place = forms.CharField(max_length=255)
    duration = forms.IntegerField()
    # photo = forms.ImageField()
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    cat = forms.ModelChoiceField(queryset=Category.objects.all())