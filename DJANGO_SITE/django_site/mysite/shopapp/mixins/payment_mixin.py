import stripe

from django.shortcuts import redirect
from django.urls import reverse

from mysite.settings import ROOT_URL


class PaymentMixin:
    root_url = ROOT_URL
    success_payment_url = 'shopapp:success'

    def __configurate(self):
        self.success_payment_url = reverse(self.success_payment_url)

    @staticmethod
    def get_pyment_methods(customer_id) -> list | None:
        payment_methods = stripe.Customer.list_payment_methods(
            customer_id,
            type="card",
        )

        if payment_methods['data']:
            return payment_methods['data']

    def make_payment(self, amount, customer, payment_method, currency='usd', confirm=True):
        self.__configurate()
        stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            automatic_payment_methods={"enabled": True},
            confirm=confirm,
            return_url=self.root_url + self.success_payment_url,
            payment_method=payment_method,
            customer=customer
        )

        return redirect(self.success_payment_url)
