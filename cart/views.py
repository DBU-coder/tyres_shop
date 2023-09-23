from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

from cart.cart import Cart
from cart.forms import AddToCartForm


class AddToCartView(View):
    product = None
    cart = None

    def dispatch(self, request, *args, **kwargs):
        self.cart = Cart(self.request)
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        self.product = content_type.model_class().objects.get(slug=product_slug)
        return super().dispatch(request, *args, **kwargs)

    def post(self, *args, **kwargs):
        form = AddToCartForm(self.request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            self.cart.add(product=self.product, quantity=cd['quantity'], update_quantity=cd['update'])
        return redirect('cart:detail')

    def get(self, *args, **kwargs):
        self.cart.add(self.product)
        return redirect(self.request.META.get('HTTP_REFERER'))


class CartDetailView(TemplateView):
    template_name = 'cart/cart_detail.html'
    extra_context = {'title': 'Shop | Cart'}

    def get(self, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        cart = Cart(self.request)
        for item in cart:
            item['update_quantity_form'] = AddToCartForm(initial={'quantity': item['quantity'], 'update': True})
        context['cart'] = cart
        return self.render_to_response(context)


class RemoveFromCartView(View):
    def get(self, request, *args, **kwargs):
        cart = Cart(self.request)
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart.remove(product)
        return redirect('cart:detail')


def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart:detail')
