from django.urls import path

from shop.views import *


app_name = 'shop'

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('category/<slug:cat_name>/', CategoryProductsListView.as_view(), name='category_products'),
    path('delivery/', DeliveryView.as_view(), name='delivery'),
    path('about/', AboutView.as_view(), name='about'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('products/<slug:ct_model>/<slug:slug>', ProductDetailView.as_view(), name='product_detail'),
]
