from itertools import chain

from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from django.views.generic import DetailView, TemplateView, ListView
from django.utils.translation import gettext_lazy as _

from enhanced_cbv.views import ListFilteredView

from cart.forms import AddToCartForm
from shop.filters import BaseFilter, TyreFilter, WheelFilter
from shop.models import HomepageProduct, Product, Category, ProductSpecification


class IndexTemplateView(TemplateView):
    template_name = 'shop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Shop | Homepage')
        context['new_products'] = HomepageProduct.objects.get_new_products('tyre', 'wheel')
        context['popular_products'] = HomepageProduct.objects.get_popular_products(days=7)
        return context


class SearchView(ListView):
    context_object_name = 'products'
    template_name = 'shop/search_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Search result')
        return context

    def get_queryset(self, **kwargs):
        search_model = self.request.GET.get('cat')
        search_query = self.request.GET.get('q')
        if not search_query:
            return []
        if search_model == 'all':
            qs = [model.objects.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            ).select_related('category').prefetch_related(
                    'gallery',
                    'ratings'
            ).annotate(
                avg_rating=Avg('ratings__value'),
                users_count=Count('ratings__ip')
            ).only('description', 'category', 'ratings', 'gallery', 'name', 'price', 'slug') for model in [Tyre, Wheel]]
            queryset = list(chain(*qs))
        else:
            ct_model = ContentType.objects.get(model=search_model)
            queryset = ct_model.model_class().objects.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            ).select_related('category').prefetch_related(
                'gallery',
                'ratings'
            ).annotate(
                avg_rating=Avg('ratings__value'),
                users_count=Count('ratings__ip')
            ).only('description', 'category', 'ratings', 'gallery', 'name', 'price', 'slug')
        return queryset


class CategoryProductsListView(ListFilteredView):
    context_object_name = 'products'
    template_name = 'shop/category_products.html'
    category_filters = {
        'tyres': TyreFilter,
        'wheels': WheelFilter
    }

    def get_filter_set(self):
        return self.category_filters.get(self.kwargs['slug'], BaseFilter)

    def get_context_data(self, **kwargs):
        category = Category.objects.get(slug=self.kwargs['slug'])
        context = super().get_context_data(**kwargs)
        context['paginate_by'] = self.paginate_by
        context['form'] = AddToCartForm
        context['title'] = f'Category | {category.name}'
        context['category'] = category
        return context

    def get_base_queryset(self):
        queryset = Product.objects.filter(category__slug=self.kwargs['slug'], is_active=True).\
            select_related('category').\
            prefetch_related('images', 'ratings', 'spec__specification').\
            annotate(
                avg_rating=Avg('ratings__value'),
                users_count=Count('ratings__ip')
            ).order_by('id')
        return queryset

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', 3)


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'shop/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddToCartForm
        context['title'] = f'Shop | {self.object.name}'
        return context


class DeliveryView(TemplateView):
    template_name = 'shop/delivery_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Shop | Delivery')
        return context


class AboutView(TemplateView):
    template_name = 'shop/about_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Shop | AboutUs')
        return context


class ContactsView(TemplateView):
    template_name = 'shop/contact_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Shop | Contacts')
        return context


def get_specifications(request, product_type_id):
    """
    Get specifications for a product type and send it to JS.
    This is necessary to select unique product specifications
    in the admin panel.
    """
    specifications = ProductSpecification.objects.filter(product_type_id=product_type_id)
    data = [{'id': spec.id, 'name': spec.name} for spec in specifications]
    return JsonResponse(data, safe=False)
