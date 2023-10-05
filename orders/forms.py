from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'country', 'zip', 'address']
        template_input_class = 'form-control rounded-0'
        widgets = {
            'first_name': forms.TextInput(attrs={'class': template_input_class}),
            'last_name': forms.TextInput(attrs={'class': template_input_class}),
            'phone': forms.TextInput(attrs={'class': template_input_class}),
            'country': forms.TextInput(attrs={'class': template_input_class}),
            'zip': forms.TextInput(attrs={'class': template_input_class}),
            'address': forms.Textarea(attrs={'class': template_input_class}),
            'email': forms.EmailInput(attrs={
                'class': template_input_class,
                'id': 'inputEmailAddress',
                'placeholder': 'user@example.com'
            }),
        }
