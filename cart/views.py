from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

from cart.cart import Cart
from cart.forms import AddToCartForm
from coupons.forms import CouponApplyForm
from shop.models import Product

CART_REDIRECT_URL = 'cart:detail'


class AddToCartView(View):
    product = None
    cart = None

    def dispatch(self, request, *args, **kwargs):
        self.cart = Cart(self.request)
        self.product = Product.objects.get(slug=self.kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)

    def post(self, *args, **kwargs):
        form = AddToCartForm(self.request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            self.cart.add(product=self.product, quantity=cd['quantity'], update_quantity=cd['update'])
        return redirect(CART_REDIRECT_URL)

    def get(self, *args, **kwargs):
        self.cart.add(self.product)
        return redirect(self.request.META.get('HTTP_REFERER'))


class CartDetailView(TemplateView):
    template_name = 'cart/cart_detail.html'
    extra_context = {'title': _('Shop | Cart')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['coupon_form'] = CouponApplyForm()
        return context


class RemoveFromCartView(View):
    def get(self, request, *args, **kwargs):
        cart = Cart(self.request)
        product = Product.objects.get(slug=kwargs.get('slug'))
        cart.remove(product)
        return redirect(CART_REDIRECT_URL)


def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect(CART_REDIRECT_URL)
