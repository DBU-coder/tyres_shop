from django import forms
from django.utils.translation import gettext_lazy as _


class CouponApplyForm(forms.Form):
    code = forms.CharField(
        label=_('Discount Code'),
        widget=forms.TextInput(attrs={'class': 'form-control rounded-0', 'placeholder': _('Enter discount code')})
    )
