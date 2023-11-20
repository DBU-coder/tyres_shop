from django import forms
from django.utils.translation import gettext_lazy as _

from shop.models import Category


class SearchForm(forms.Form):
    q = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control w-100', 'placeholder': _('Search for Products')})
    )
    cat = forms.ModelChoiceField(
        label='',
        queryset=Category.objects.all(),
        empty_label=_('All Categories'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select flex-shrink-0', 'style': 'width: 10.5rem;'})
    )
