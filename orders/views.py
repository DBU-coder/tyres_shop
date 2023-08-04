from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, TemplateView
from django.contrib.admin.views.decorators import staff_member_required

from cart.cart import Cart
from customers.models import Customer
from orders.forms import OrderCreateForm
from orders.models import OrderItem, Order


class OrderCreateView(CreateView):
    template_name = 'orders/order/order_create.html'
    form_class = OrderCreateForm
    title = 'Store - Оформление заказа'

    def get_initial(self):
        user = self.request.user
        user_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'address': user.address
        }
        return user_data

    def form_valid(self, form):
        cart = Cart(self.request)
        order = form.save(commit=False)
        customer = Customer.objects.get(pk=self.request.user.pk)
        order.customer = customer
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
        return super().form_valid(form)

# TODO: Сделать оплату сразу после отправки формы.
    def get_success_url(self):
        return reverse_lazy('orders:order_shipping', args=[self.object.id])


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

