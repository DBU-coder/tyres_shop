from django.views.generic.detail import SingleObjectMixin

from shop.models import *


class CategoryDetailMixin(SingleObjectMixin):
    CATEGORY_SLUG2PRODUCT_MODEL = {
        'tyres': Tyre,
        'wheels': Wheel
    }

    def get_context_data(self, **kwargs):
        if isinstance(self.get_object(), Category):
            model = self.CATEGORY_SLUG2PRODUCT_MODEL[self.get_object().slug]
            context = super().get_context_data(**kwargs)
            context['cats'] = Category.objects.all()
            context['category_products'] = model.objects.all()
            return context
        context = super().get_context_data(**kwargs)
        return context
