from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, TemplateView, ListView
from enhanced_cbv.views import ListFilteredView

from cart.forms import AddToCartForm
from shop.filters import BaseFilter, TyreFilter, WheelFilter
from shop.forms import SearchForm
from shop.models import HomepageProduct, Product, Category, ProductSpecification


class IndexTemplateView(TemplateView):
    template_name = 'shop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Shop | Homepage')
        context['new_products'] = HomepageProduct.objects.get_new_products(quantity=10)
        context['popular_products'] = HomepageProduct.objects.get_popular_products(days=7)
        context['search_form'] = SearchForm()
        return context


class SearchView(ListView):
    context_object_name = 'products'
    template_name = 'shop/search_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Search result')
        context['search_form'] = SearchForm()
        return context

    def get_queryset(self, **kwargs):
        category_id = self.request.GET.get('cat')
        search_query = self.request.GET.get('q')
        if not search_query:
            return []
        if not category_id:
            queryset = Product.objects.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            ).select_related('category').prefetch_related(
                'images',
                'ratings'
            ).annotate(
                avg_rating=Avg('ratings__value'),
                users_count=Count('ratings__ip')
            ).only('description', 'category', 'ratings', 'images', 'name', 'price', 'slug')
        else:
            queryset = Product.objects.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query),
                category_id=category_id,
            ).select_related('category').prefetch_related(
                'images',
                'ratings'
            ).annotate(
                avg_rating=Avg('ratings__value'),
                users_count=Count('ratings__ip')
            ).only('description', 'category', 'ratings', 'images', 'name', 'price', 'slug')
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
        context['search_form'] = SearchForm()
        return context

    def get_base_queryset(self):
        queryset = Product.objects.filter(category__slug=self.kwargs['slug'], is_active=True). \
            select_related('category'). \
            prefetch_related('images', 'ratings', 'spec__specification'). \
            annotate(
            avg_rating=Avg('ratings__value'),
            users_count=Count('ratings__ip')
        ).order_by('id')
        return queryset

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', 3)


class ProductDetailView(DetailView):
    context_object_name = 'product'
    template_name = 'shop/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddToCartForm
        context['title'] = f'Shop | {self.object.name}'
        context['search_form'] = SearchForm()
        return context

    def get_queryset(self):
        queryset = Product.objects.select_related('category'). \
            prefetch_related('images', 'ratings', 'spec__specification'). \
            annotate(
                avg_rating=Avg('ratings__value'),
                users_count=Count('ratings__ip')
            )
        return queryset




class DeliveryView(TemplateView):
    template_name = 'shop/delivery_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Shop | Delivery')
        context['search_form'] = SearchForm()
        return context


class AboutView(TemplateView):
    template_name = 'shop/about_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Shop | AboutUs')
        context['search_form'] = SearchForm()
        return context


class ContactsView(TemplateView):
    template_name = 'shop/contact_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Shop | Contacts')
        context['search_form'] = SearchForm()
        return context


def get_specifications(_, product_type_id):
    """
    Get specifications for a product type and send it to JS.
    This is necessary to select unique product specifications
    in the admin panel.
    """
    specifications = ProductSpecification.objects.filter(product_type_id=product_type_id)
    data = [{'id': spec.id, 'name': spec.name} for spec in specifications]
    return JsonResponse(data, safe=False)
