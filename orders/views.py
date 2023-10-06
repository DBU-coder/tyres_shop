from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DeleteView
from formtools.wizard.views import SessionWizardView

from cart.cart import Cart
from customers.models import Customer
from orders.forms import OrderCreateForm, OrderAddressForm, OrderDeliveryMethodForm
from orders.models import Order, OrderItem


class OrderCreateView(SessionWizardView):
    form_list = [OrderCreateForm, OrderAddressForm, OrderDeliveryMethodForm]

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
        cart = Cart(self.request)
        customer = Customer.objects.get(pk=self.request.user.pk)
        receiver_form = form_list[0]
        order = receiver_form.save(commit=False)
        order.customer = customer
        address_form = form_list[1]
        order.country = address_form.cleaned_data['country']
        order.zip = address_form.cleaned_data['zip']
        order.address = address_form.cleaned_data['address']
        delivery_form = form_list[-1]
        order.delivery = delivery_form.cleaned_data['delivery']
        order.save()
        for item in cart:
            OrderItem.objects.create(order=order,
                                     content_object=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity'])
        # Очищаем корзину.
        cart.clear()
        # Запуск асинхронной задачи.
        # order_created.delay(order.id)
        return HttpResponseRedirect(reverse_lazy('payments:create', args=[order.id]))


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'orders/order/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('orders:order_list')


class ShippingChoiceView(TemplateView):
    template_name = 'orders/order/shipping_choice.html'


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


@staff_member_required
def admin_order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/order_details.html', {'order': order})
