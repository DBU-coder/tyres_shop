from django import forms
from django.utils.translation import gettext_lazy as _


class AddToCartForm(forms.Form):

    CHOICE_PRODUCT_QUANTITY = [(i, str(i)) for i in range(1, 11)]

    quantity = forms.TypedChoiceField(
        label=_('Quantity'),
        choices=CHOICE_PRODUCT_QUANTITY,
        coerce=int,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )
    update = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )
