from http import HTTPStatus

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404

import stripe
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from orders.models import Order
from shop.models import ProductStatistic

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreatePaymentView(View):
    """
    Create a checkout session and redirect the user to Stripe's checkout page
    """

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(id=self.kwargs['order_id'])

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=order.stripe_products(),
            metadata={'order_id': order.id},
            mode="payment",
            success_url=f'{settings.DOMAIN_NAME}{reverse("payments:success")}',
            cancel_url=f'{settings.DOMAIN_NAME}{reverse("payments:cancel")}',
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(View):
    """
    Stripe webhook view to handle checkout session completed event.
    """
    order = None

    def post(self, request):
        payload = request.body
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError:
            # Invalid payload
            return HttpResponse(status=HTTPStatus.BAD_REQUEST)
        except stripe.error.SignatureVerificationError:
            # Invalid signature
            return HttpResponse(status=HTTPStatus.BAD_REQUEST)

        if event["type"] == "checkout.session.completed":
            session = event.data.object

            self.set_order_paid(session)
            self.set_sales_quantity()
        # Can handle other events here.

        return HttpResponse(status=HTTPStatus.OK)

    def set_order_paid(self, session):
        order_id = session.metadata.order_id
        self.order = get_object_or_404(Order, id=order_id)
        self.order.paid = True
        self.order.save()

    def set_sales_quantity(self):
        for item in self.order.items.all():
            obj, _ = ProductStatistic.objects.get_or_create(
                content_type=item.content_type,
                object_id=item.object_id,
                date=timezone.now(),
                defaults={'content_type': item.content_type, 'object_id': item.object_id, 'date': timezone.now()},
            )
            obj.sales_quantity += item.quantity
            obj.save(update_fields=['sales_quantity'])


class SuccessView(TemplateView):
    template_name = 'payments/success.html'


class CancelView(TemplateView):
    template_name = 'payments/cancel.html'
