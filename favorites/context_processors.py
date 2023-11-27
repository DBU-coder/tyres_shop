from .utils import Favorite


def favorites(request):
    return {'favorites': Favorite(request)}
