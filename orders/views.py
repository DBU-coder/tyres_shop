from http import HTTPStatus

import stripe
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView, DeleteView
from formtools.wizard.views import SessionWizardView

from cart.cart import Cart
from customers.models import Customer
from orders.forms import OrderCreateForm, OrderAddressForm, OrderDeliveryMethodForm
from orders.models import Order, OrderItem
from shop.models import ProductStatistic


class OrderCreateView(SessionWizardView):
    form_list = [OrderCreateForm, OrderAddressForm, OrderDeliveryMethodForm]
    template_name = 'orders/order/order_create.html'

    def get_form_initial(self, step):
        user = self.request.user
        initial = self.initial_dict.get(step, {})
        initial.update(
            {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': user.phone,
                'address': user.address
            }
        )
        return initial

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        context['title'] = 'Shop|Checkout'
        return context

    def done(self, form_list, **kwargs):
        order = form_list[0].save(commit=False)
        order.customer = Customer.objects.get(pk=self.request.user.pk)
        order.country = form_list[1].cleaned_data['country']
        order.zip = form_list[1].cleaned_data['zip']
        order.address = form_list[1].cleaned_data['address']
        order.delivery = form_list[-1].cleaned_data['delivery']
        order.save()

        cart = Cart(self.request)
        for item in cart:
            OrderItem.objects.create(order=order,
                                     content_object=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity'])
        # Очищаем корзину.
        cart.clear()
        # Запуск асинхронной задачи.
        # order_created.delay(order.id)

        # Create a checkout session and redirect the user to Stripe's checkout page
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=order.stripe_products(),
            metadata={'order_id': order.id},
            mode="payment",
            success_url=f'{settings.DOMAIN_NAME}{reverse("orders:success")}',
            cancel_url=f'{settings.DOMAIN_NAME}{reverse("orders:cancel")}',
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'orders/order/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('orders:order_list')


class OrdersListView(ListView):
    template_name = 'orders/order/user_orders.html'
    context_object_name = 'orders'
    extra_context = {'title': 'Shop|Orders'}

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)


class OrderDetailsView(ListView):
    template_name = 'orders/order/order_details.html'
    context_object_name = 'order'

    def get_queryset(self):
        order = Order.objects.get(id=self.kwargs['order_id'])
        return order.items.all()


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
    template_name = 'orders/payments/success.html'


class CancelView(TemplateView):
    template_name = 'orders/payments/cancel.html'


@staff_member_required
def admin_order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/order_details.html', {'order': order})
