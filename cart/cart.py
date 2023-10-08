import copy

from django.conf import settings
from django.contrib.contenttypes.models import ContentType


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart_data = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product.model_name not in self.cart_data:
            self.cart_data[product.model_name] = {}
        if product_id not in self.cart_data[product.model_name]:
            self.cart_data[product.model_name].update({product_id: {'quantity': 0, 'price': product.price}})
        if update_quantity:
            self.cart_data[product.model_name][product_id]['quantity'] = quantity
        else:
            self.cart_data[product.model_name][product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if self.cart_data[product.model_name] and product_id in self.cart_data[product.model_name]:
            del self.cart_data[product.model_name][product_id]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True

    def __len__(self):
        quantity = []
        for products in self.cart_data.values():
            for item in products.values():
                quantity.append(item['quantity'])
        return sum(quantity)

    def __iter__(self):
        cart_data = copy.deepcopy(self.cart_data)
        model_names = cart_data.keys()
        for model_name in model_names:
            product_ids = cart_data[model_name].keys()
            product_type = ContentType.objects.get(model=model_name)
            product_model = product_type.model_class()
            products = product_model.objects.filter(id__in=product_ids)
            for product in products:
                item = cart_data[model_name][str(product.id)]
                item['product'] = product
                item['total_price'] = item['price'] * item['quantity']
                yield item

    def get_total_price(self):
        return sum([product['total_price']for product in self])
