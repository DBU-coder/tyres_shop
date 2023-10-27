from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext_lazy as _

from allauth.account.forms import LoginForm, SignupForm, ChangePasswordForm

from .models import Customer


class CustomerSingUpForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'user@example.com'})
        self.fields['email'].label = _('Email')
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].label = _('Password')
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].label = _('Confirm Password')

        self.fields['phone'] = forms.CharField(
            label=_('Phone'),
            required=True,
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+380123456789'})
        )

        self.fields['first_name'] = forms.CharField(
            label=_('First name'),
            required=True,
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )

        self.fields['last_name'] = forms.CharField(
            label=_('Last name'),
            required=True,
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )

    def save(self, request):
        user = super().save(request)
        user.phone = self.cleaned_data.pop('phone')
        user.first_name = self.cleaned_data.pop('first_name')
        user.last_name = self.cleaned_data.pop('last_name')
        return user


class CustomerLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if field_name == 'remember':
                field.widget.attrs.update({'class': 'form-check-input mt-1'})
        self.fields['password'].label = _('Password')


class CustomerUpdateForm(UserChangeForm):

    email = forms.EmailField(
        label=_('Email'),
        disabled=True,
        widget=forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'inputEmailAddress',
                'placeholder': 'user@example.com'
            })
    )
    first_name = forms.CharField(
        label=_('First name'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label=_('Last name'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        label=_('Phone'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        label=_('Address'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'email', 'phone', 'address')


class CustomerChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['oldpassword'].widget.attrs.update({'class': 'form-control'})
        self.fields['oldpassword'].label = _('Old password')
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].label = _('New password')
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].label = _('Repeat password')

