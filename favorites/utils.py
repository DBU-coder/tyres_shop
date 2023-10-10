from django.conf import settings


class Favorite:
    def __init__(self, request):
        self.session = request.session
        favorites = self.session.get(settings.FAVORITES_SESSION_ID)
        if not favorites:
            favorites = self.session[settings.FAVORITES_SESSION_ID] = dict()
        self.favorite_items = favorites

    def add(self, product):
        product_id = str(product.id)
        ids = self.favorite_items.get(product.model_name)
        if not ids:
            self.favorite_items[product.model_name] = [product_id]
        else:
            ids.append(product_id)
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        ids = self.favorite_items[product.model_name]
        if product_id in ids:
            ids.remove(product_id)
            self.save()

    def save(self):
        self.session.modified = True


