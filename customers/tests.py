from django.test import TestCase

from customers.models import Customer


class TestCustomerModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        Customer.objects.create(email='test@example.com', password='Test12345Password')

    def test_get_absolute_url(self):
        customer = Customer.objects.get(pk=1)
        self.assertEquals(customer.get_absolute_url(), '/customers/profile/1/details/')
