from django.urls import path

from cart.views import CartDetailView, AddToCartView, RemoveFromCartView, clear_cart


app_name = 'cart'

urlpatterns = [
    path('', CartDetailView.as_view(), name='cart_detail'),
    path('add/<str:ct_model>/<str:slug>', AddToCartView.as_view(), name='cart_add'),
    path('remove/<str:ct_model>/<str:slug>', RemoveFromCartView.as_view(), name='remove'),
    path('clear/', clear_cart, name='clear'),
]
