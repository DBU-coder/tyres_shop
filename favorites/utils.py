from django.conf import settings


class Favorite:

    def __init__(self, request):
        self.session = request.session
        favorites = self.session.get(settings.FAVORITES_SESSION_ID)
        if not favorites:
            favorites = self.session[settings.FAVORITES_SESSION_ID] = dict()
        self.favorite_items = favorites

    def add(self, product_type: str, product_id: int):
        ids = self.favorite_items.setdefault(product_type, [])
        if product_id not in ids:
            ids.append(product_id)
            self.save()

    def remove(self, product_type: str, product_id: int):
        ids = self.favorite_items[product_type]
        if product_id in ids:
            ids.remove(product_id)
            if len(ids) == 0:
                del self.favorite_items[product_type]
            self.save()

    def clear(self):
        del self.session[settings.FAVORITES_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True


