import django_filters as filters
from django import forms
from django.forms import HiddenInput
from django.utils.translation import gettext_lazy as _
from django_filters.widgets import LinkWidget, RangeWidget

from .models import ProductSpecificationValue, Product


class PriceRangeSliderWidget(RangeWidget):
    template_name = 'shop/filter_widgets/price_range_slider_widget.html'

    class Media:
        css = {
            'all': ('assets/plugins/nouislider/nouislider.min.css',)
        }
        js = ('assets/plugins/nouislider/nouislider.min.js',)

    def __init__(self, attrs=None, min_value=0, max_value=1000, step=1):
        widgets = (forms.TextInput, forms.TextInput)
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        super(RangeWidget, self).__init__(widgets, attrs=attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['min_value'] = self.min_value
        context['max_value'] = self.max_value
        context['step'] = self.step
        return context

    def format_value(self, value):
        return str(value)


class PriceRangeFilter(filters.RangeFilter):
    def __init__(self, products, *args, **kwargs):
        super().__init__(*args, **kwargs)
        price_values = [p.price for p in products]
        min_value = min(price_values)
        max_value = max(price_values)
        self.extra['widget'] = PriceRangeSliderWidget(
            min_value=min_value,
            max_value=max_value,
            step=1,
            attrs={'class': 'form-control rounded-0'}
        )


class BaseFilter(filters.FilterSet):
    ORDERING_CHOICES = (
        ('-avg_rating', _('Sort by rating:high to low')),
        ('avg_rating', _('Sort by rating:low to high')),
        ('-created', _('Sort by newest')),
        ('price', _('Sort by price:low to high')),
        ('-price', _('Sort by price:high to low')),
    )

    ordering = filters.ChoiceFilter(
        label=_('Sort by:'),
        choices=ORDERING_CHOICES,
        method='filter_by_order',
        empty_label=_('Default sorting'),
        widget=forms.Select(attrs={'class': 'form-select ms-3 rounded-0', 'onchange': 'form.submit()'})
    )

    brand = filters.MultipleChoiceFilter(
        label=_('Brands'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['price'] = PriceRangeFilter(field_name='price', label=_('Price'), products=self.queryset)
        self.filters['brand'].extra['choices'] = [(brand, brand) for brand in sorted(
            self.queryset.order_by().values_list('brand', flat=True).distinct()
        )]

    def filter_by_order(self, queryset, name, value):
        """
        Order queryset by user choice.
        """
        return queryset.order_by(value)

    def get_spec_value_choices(self, spec_name: str):
        """
        Returns a list of tuples with unique
        values for a given specification name.
        """
        spec_values = ProductSpecificationValue.objects.filter(
            specification__name__iexact=spec_name,
            product__in=self.queryset,
        ).values_list('value', flat=True).distinct('value')
        return [(s, s.title()) for s in sorted(spec_values)]


class TyreFilter(BaseFilter):
    vehicle = filters.ChoiceFilter(
        label=_('Vehicle'),
        field_name='spec__value',
        lookup_expr='iexact',
        widget=LinkWidget(attrs={'class': 'list-unstyled mb-0 categories-list'})
    )
    diameter = filters.MultipleChoiceFilter(
        label=_('Diameter'),
        field_name='spec__value',
        lookup_expr='iexact',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )

    season = filters.ChoiceFilter(
        label=_('Season'),
        field_name='spec__value',
        lookup_expr='iexact',
        empty_label=_('All tyres'),
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['vehicle'].extra['choices'] = self.get_spec_value_choices('vehicle')
        self.filters['diameter'].extra['choices'] = self.get_spec_value_choices('diameter')
        self.filters['season'].extra['choices'] = self.get_spec_value_choices('season')


class WheelFilter(BaseFilter):
    diameter = filters.MultipleChoiceFilter(
        label=_('Diameter'),
        field_name='spec__value',
        lookup_expr='iexact',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    width = filters.ChoiceFilter(
        label=_('Width'),
        field_name='spec__value',
        lookup_expr='iexact',
        empty_label=_('All'),
    )
    dia = filters.ChoiceFilter(
        label='DIA',
        field_name='spec__value',
        lookup_expr='iexact',
        empty_label=_('All'),
    )
    psd = filters.ChoiceFilter(
        label='PSD',
        field_name='spec__value',
        lookup_expr='iexact',
        empty_label=_('All'),
    )
    et = filters.ChoiceFilter(
        label='ET',
        field_name='spec__value',
        lookup_expr='iexact',
        empty_label=_('All'),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['width'].extra['choices'] = self.get_spec_value_choices('width')
        self.filters['diameter'].extra['choices'] = self.get_spec_value_choices('diameter')
        self.filters['dia'].extra['choices'] = self.get_spec_value_choices('dia')
        self.filters['psd'].extra['choices'] = self.get_spec_value_choices('psd')
        self.filters['et'].extra['choices'] = self.get_spec_value_choices('et')
