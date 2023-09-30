import json

from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from ratings.models import Rating


class SetRatingView(View):
    """Logged users only can set rating."""

    def get_user_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        request_data = json.loads(request.body)
        ct_model = ContentType.objects.get(model=request_data['product_model'])
        Rating.objects.update_or_create(
            ip=self.get_user_ip(),
            content_type=ct_model,
            object_id=request_data['product_id'],

            defaults={'value': request_data['user_rating']}
        )
        product = ct_model.get_object_for_this_type(id=request_data['product_id'])
        new_rating = product.ratings.aggregate(avg_value=Avg('value'))
        response_data = {
            'new_rating': round(new_rating['avg_value'], 1),
        }
        return JsonResponse(data=response_data)





