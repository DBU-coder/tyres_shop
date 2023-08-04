from django import template
from django.db.models import Avg, Count

from shop.models import Category

menu = [
    {'name': 'Delivery', 'url_name': 'shop:delivery'},
    {'name': 'About', 'url_name': 'shop:about'},
    {'name': 'Contact us', 'url_name': 'shop:contacts'},
]

register = template.Library()


@register.simple_tag()
def get_main_image(product):
    gallery = product.gallery.first()
    return gallery.image


@register.inclusion_tag('menu.html')
def get_menu():
    cats = Category.objects.all()
    return {'menu': menu, 'cats': cats}


@register.inclusion_tag('rating.html')
def show_rating(product):
    ratings = product.ratings.aggregate(avg_value=Avg('value',  default=0), users_count=Count('ip'))
    data = {
        'product_id': product.id,
        'product_model': product.model_name,
        'rating': round(ratings['avg_value'], 1),
        'users_count': ratings['users_count']
    }
    return data


@register.simple_tag()
def reviews(product):
    return product.ratings.count()


# Needed for filtering/sorting with pagination.
@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Return encoded URL parameters that are the same as the current
    request's parameters, only with the specified GET parameters added or changed.

    It also removes any empty parameters to keep things neat,
    so you can remove a parm by setting it to ``""``.

    For example, if you're on the page ``/things/?with_frosting=true&page=5``,
    then

    <a href="/things/?{% param_replace page=3 %}">Page 3</a>

    would expand to

    <a href="/things/?with_frosting=true&page=3">Page 3</a>

    Based on
    https://stackoverflow.com/questions/22734695/next-and-before-links-for-a-django-paginated-query/22735278#22735278
    """
    params = context['request'].GET.copy()
    for k, v in kwargs.items():
        params[k] = v
    for k in [k for k, v in params.items() if not v]:
        del params[k]
    return params.urlencode()
