from django.conf import settings


class Favorite:

    def __init__(self, request):
        self.session = request.session
        favorites = self.session.get(settings.FAVORITES_SESSION_ID)
        if not favorites:
            favorites = self.session[settings.FAVORITES_SESSION_ID] = list()
        self.favorite_items = favorites

    def __len__(self):
        return len(self.favorite_items)

    def add(self, product_id: int):
        if product_id not in self.favorite_items:
            self.favorite_items.append(product_id)
            self.save()

    def remove(self, product_id: int):
        if product_id in self.favorite_items:
            self.favorite_items.remove(product_id)
            self.save()

    def clear(self):
        del self.session[settings.FAVORITES_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True
