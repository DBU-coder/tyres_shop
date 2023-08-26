from django.db.models import Avg
from django.views.generic import DetailView, TemplateView

from enhanced_cbv.views import ListFilteredView

from cart.forms import AddToCartForm
from shop.filters import TyreFilter, WheelFilter
from shop.models import HomepageProduct, Tyre, Wheel, Category


class IndexTemplateView(TemplateView):
    template_name = 'shop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Shop | Homepage'
        context['new_products'] = HomepageProduct.objects.get_new_products('tyre', 'wheel')
        context['popular_products'] = HomepageProduct.objects.get_popular_products(days=7)
        return context


class CategoryProductsListView(ListFilteredView):
    CT_MODELS_MODEL_CLASS = {
        'tyres': Tyre,
        'wheels': Wheel
    }

    context_object_name = 'products'
    template_name = 'shop/category_products.html'

    def get_filter_set(self):
        if self.kwargs['cat_name'] == 'tyres':
            return TyreFilter
        return WheelFilter

    def get_context_data(self, **kwargs):
        category = Category.objects.get(slug=self.kwargs.get('cat_name'))
        context = super().get_context_data(**kwargs)
        context['paginate_by'] = self.paginate_by
        context['category'] = category
        context['title'] = f'Category | {category.name}'
        return context

    def get_base_queryset(self):
        ct_model = self.kwargs.get('cat_name')
        product_model = self.CT_MODELS_MODEL_CLASS[ct_model]
        queryset = product_model.objects.annotate(avg_rating=Avg('ratings__value'))
        return queryset

    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', 3)


class ProductDetailView(DetailView):
    CT_MODELS_MODEL_CLASS = {
        'tyre': Tyre,
        'wheel': Wheel
    }
    context_object_name = 'product'
    template_name = 'shop/product_detail.html'

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODELS_MODEL_CLASS[kwargs['ct_model']]
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddToCartForm
        context['ct_model'] = self.model._meta.model_name
        context['title'] = f'Shop | {self.object.name}'
        return context


class DeliveryView(TemplateView):
    template_name = 'shop/delivery_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Shop | Delivery'
        return context


class AboutView(TemplateView):
    template_name = 'shop/about_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Shop | AboutUs'
        return context


class ContactsView(TemplateView):
    template_name = 'shop/contact_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Shop | Contacts'
        return context
