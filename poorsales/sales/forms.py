from django import forms
from django.core.exceptions import ValidationError
from .models import *


class AddSaleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Не выбрано'

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'title': forms.Textarea(attrs={'class': 'form-input', 'rows': 1}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }

    def clear_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')

        return title
