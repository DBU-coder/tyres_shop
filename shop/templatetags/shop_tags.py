from django import template
from django.core.cache import cache

from shop.models import Category

menu = [
    {'name': 'Delivery', 'url_name': 'shop:delivery'},
    {'name': 'About', 'url_name': 'shop:about'},
    {'name': 'Contact us', 'url_name': 'shop:contacts'},
]

register = template.Library()


@register.simple_tag()
def get_main_image(product):
    try:
        first_gallery_obj = product.gallery.all()[0]
        return first_gallery_obj.image
    except IndexError:
        return None


@register.inclusion_tag('menu.html')
def get_menu():
    cats = cache.get('cats')
    if not cats:
        cats = Category.objects.all()
        cache.set('cats', cats, 60 * 5)
    return {'menu': menu, 'cats': cats}


@register.inclusion_tag('rating.html')
def show_rating(product):
    data = {
        'product_id': product.id,
        'product_model': product.model_name,
        'rating': round(product.avg_rating, 1) if product.avg_rating else 0,
        'users_count': product.users_count if product.users_count else 0
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
