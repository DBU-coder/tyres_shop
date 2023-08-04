from django import forms


class AddToCartForm(forms.Form):

    CHOICE_PRODUCT_QUANTITY = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

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
