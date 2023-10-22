import django_filters as filters
from django import forms
from django.utils.translation import gettext_lazy as _
from django_filters.widgets import LinkWidget, RangeWidget

from shop.models import Tyre, Wheel


class BaseFilter(filters.FilterSet):
    ORDERING_CHOICES = (
        ('-avg_rating', _('Sort by rating:high to low')),
        ('avg_rating', _('Sort by rating:low to high')),
        ('-created', _('Sort by newest')),
        ('price', _('Sort by price:low to high')),
        ('-price', _('Sort by price:high to low')),
    )

    price = filters.RangeFilter(
        label=_('Price'),
        widget=RangeWidget(attrs={'size': 7})
    )
    brand = filters.MultipleChoiceFilter(
        label=_('Brands'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    diameter = filters.MultipleChoiceFilter(
        label=_('Diameter'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    ordering = filters.ChoiceFilter(
        label=_('Sort by:'),
        choices=ORDERING_CHOICES,
        method='filter_by_order',
        empty_label=_('Default sorting'),
        widget=forms.Select(attrs={'class': 'form-select ms-3 rounded-0', 'onchange': 'form.submit()'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.filters['brand'].extra['choices'] = [(brand, brand) for brand in sorted(
                self.queryset.values_list('brand', flat=True).distinct()
            )]

        self.filters['diameter'].extra['choices'] = [(d, f'R {d}') for d in sorted(
                self.queryset.values_list('diameter', flat=True).distinct()
            )]

    def filter_by_order(self, queryset, name, value):
        return queryset.order_by(value)


class TyreFilter(BaseFilter):
    vehicle_type = filters.ChoiceFilter(
        label=_('Vehicle'),
        choices=Tyre.VEHICLE_CHOICES,
        widget=LinkWidget(attrs={'class': 'list-unstyled mb-0 categories-list'})
    )
    season = filters.ChoiceFilter(
        label=_('Season'),
        choices=Tyre.SEASON_CHOICES,
        empty_label=_('All tyres'),
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Tyre
        fields = ['vehicle_type', 'season']


class WheelFilter(BaseFilter):
    type = filters.ChoiceFilter(
        label=_('Type'),
        choices=Wheel.TYPE_CHOICES,
        widget=LinkWidget(attrs={'class': 'list-unstyled mb-0 categories-list'})
    )

    class Meta:
        model = Wheel
        fields = ['type']
