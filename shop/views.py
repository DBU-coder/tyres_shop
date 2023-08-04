from django.db.models import Avg
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import DetailView, ListView, TemplateView

from cart.forms import AddToCartForm
from shop.models import *


class IndexListView(ListView):
    template_name = 'shop/index.html'
    model = HomepageProduct
    context_object_name = 'latest_products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Shop | Homepage'
        return context

    def get_queryset(self):
        return HomepageProduct.objects.get_products('tyre', 'wheel')


class CategoryProductsListView(ListView):
    CT_MODELS_MODEL_CLASS = {
        'tyres': Tyre,
        'wheels': Wheel
    }

    context_object_name = 'products'
    template_name = 'shop/category_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_field'] = self.order_field
        context['paginate_by'] = self.paginate_by
        context['title'] = f'Category | {self.kwargs.get("cat_name").title()}'
        return context

    def get_queryset(self):
        ct_model = self.kwargs.get('cat_name')
        self.order_field = self.request.GET.get('order_by', 'id')
        product_model = self.CT_MODELS_MODEL_CLASS[ct_model]
        queryset = product_model.objects.annotate(avg_rating=Avg('ratings__value')).order_by(self.order_field)
        print(self.order_field)
        print(queryset)
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
