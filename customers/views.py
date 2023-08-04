from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView

from .forms import CustomerUpdateForm, CustomerChangePasswordForm
from .models import Customer


class ProfileDetailView(DetailView):
    model = Customer
    template_name = 'customers/profile.html'


class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerUpdateForm
    template_name = 'customers/customer_details.html'
    extra_context = {'title': 'Shop | Customer Details'}


class CustomerChangePassword(PasswordChangeView):
    template_name = 'customers/../templates/account/change_password.html'
    form_class = CustomerChangePasswordForm

    def get_success_url(self):
        return reverse_lazy('customers:profile', args=[self.request.user.id])

