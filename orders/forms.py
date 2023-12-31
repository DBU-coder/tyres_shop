from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Order, Delivery


class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone']
        template_input_class = 'form-control rounded-0'
        widgets = {
            'first_name': forms.TextInput(attrs={'class': template_input_class}),
            'last_name': forms.TextInput(attrs={'class': template_input_class}),
            'phone': forms.TextInput(attrs={'class': template_input_class}),
            'email': forms.EmailInput(attrs={
                'class': template_input_class,
                'id': 'inputEmailAddress',
                'placeholder': 'user@example.com'
            }),
        }


class OrderAddressForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['country', 'zip', 'address']
        template_input_class = 'form-control rounded-0'
        widgets = {
            'country': forms.TextInput(attrs={'class': template_input_class}),
            'zip': forms.TextInput(attrs={'class': template_input_class}),
            'address': forms.Textarea(attrs={'class': template_input_class}),
        }


class OrderDeliveryMethodForm(forms.ModelForm):
    delivery = forms.ModelChoiceField(
        queryset=Delivery.objects.all(),
        empty_label=None,
        label=_('Choose method'),
        widget=forms.RadioSelect()
    )

    class Meta:
        model = Order
        fields = ['delivery']
