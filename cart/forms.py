from django import forms


class AddToCartForm(forms.Form):

    CHOICE_PRODUCT_QUANTITY = [(i, str(i)) for i in range(1, 11)]

    quantity = forms.TypedChoiceField(
        label='Quantity',
        choices=CHOICE_PRODUCT_QUANTITY,
        coerce=int,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )
    update = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )
