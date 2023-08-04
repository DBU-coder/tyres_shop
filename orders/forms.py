from django import forms
from django.contrib.contenttypes.models import ContentType

from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'country', 'zip', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control rounded-0'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control rounded-0'}),
            'phone': forms.TextInput(attrs={'class': 'form-control rounded-0'}),
            'country': forms.TextInput(attrs={'class': 'form-control rounded-0'}),
            'zip': forms.TextInput(attrs={'class': 'form-control rounded-0'}),
            'address': forms.Textarea(attrs={'class': 'form-control rounded-0'}),
            'email': forms.EmailInput(attrs={
                'class': 'form-control rounded-0',
                'id': 'inputEmailAddress',
                'placeholder': 'user@example.com'
            }),
        }

