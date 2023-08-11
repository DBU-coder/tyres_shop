import django_filters as filters
from django import forms
from django_filters.widgets import LinkWidget, RangeWidget

from shop.models import Tyre, Wheel


class BaseFilter(filters.FilterSet):
    ORDERING_CHOICES = (
        ('-avg_rating', 'Sort by rating:high to low'),
        ('avg_rating', 'Sort by rating:low to high'),
        ('-created', 'Sort by newest'),
        ('price', 'Sort by price:low to high'),
        ('-price', 'Sort by price:high to low'),
    )

    price = filters.RangeFilter(widget=RangeWidget(attrs={'size': 7}))
    brand = filters.MultipleChoiceFilter(
        label='Brands',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    ordering = filters.ChoiceFilter(
        label='Sort by:',
        choices=ORDERING_CHOICES,
        method='filter_by_order',
        empty_label='Default sorting',
        widget=forms.Select(attrs={'class': 'form-select ms-3 rounded-0', 'onchange': 'form.submit()'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        model = self.queryset.model
        self.filters['brand'].extra['choices'] = [(brand, brand) for brand in
                                                  sorted(model.objects.values_list('brand', flat=True).distinct())]
        self.filters['diameter'].extra['choices'] = [(d, f'R {d}') for d in
                                                     sorted(model.objects.values_list('diameter', flat=True).distinct())]

    def filter_by_order(self, queryset, name, value):
        return queryset.order_by(value)


class TyreFilter(BaseFilter):
    vehicle_type = filters.ChoiceFilter(
        label='Vehicle',
        choices=Tyre.VEHICLE_CHOICES,
        widget=LinkWidget(attrs={'class': 'list-unstyled mb-0 categories-list'})
    )
    season = filters.ChoiceFilter(
        choices=Tyre.SEASON_CHOICES,
        empty_label='All tyres',
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    diameter = filters.MultipleChoiceFilter(
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Tyre
        fields = ['price', 'brand', 'vehicle_type', 'season']


class WheelFilter(BaseFilter):
    type = filters.ChoiceFilter(
        choices=Wheel.TYPE_CHOICES,
        widget=LinkWidget(attrs={'class': 'list-unstyled mb-0 categories-list'})
    )
    diameter = filters.MultipleChoiceFilter(
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Wheel
        fields = ['price', 'brand', 'diameter', 'type']


