import copy
from decimal import Decimal

from django.conf import settings
from django.core.cache import cache

from cart.forms import AddToCartForm
from coupons.models import Coupon
from shop.models import Product


class Cart:
    CACHE_KEY = 'cart_products'

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart_data = cart
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart_data:
            self.cart_data[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart_data[product_id]['quantity'] = quantity
        else:
            self.cart_data[product_id]['quantity'] += quantity
        cache.delete(self.CACHE_KEY)
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart_data:
            del self.cart_data[product_id]
            cache.delete(self.CACHE_KEY)
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True

    def __len__(self):
        return sum(data['quantity'] for data in self.cart_data.values())

    def __iter__(self):
        cart_data = copy.deepcopy(self.cart_data)
        product_ids = list(cart_data.keys())
        products = cache.get_or_set(
            key=self.CACHE_KEY,
            timeout=300,
            default=Product.objects.prefetch_related('images').filter(id__in=product_ids)
        )
        for product in products:
            item = cart_data[str(product.id)]
            item['product'] = product
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            item['update_quantity_form'] = AddToCartForm(initial={'quantity': item['quantity'], 'update': True})
            yield item

    def get_total_price(self):
        return sum([product['total_price']for product in self])

    @property
    def coupon(self):
        coupon = None
        if self.coupon_id:
            try:
                coupon = Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return coupon

    def get_discount(self):
        if self.coupon:
            discount = (self.coupon.discount / Decimal(100)) * self.get_total_price()
            return round(discount, 1)
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
