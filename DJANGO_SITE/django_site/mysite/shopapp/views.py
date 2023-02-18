import random

from typing import Tuple
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.views import View
from django.shortcuts import redirect, render
from django.views.generic import ListView, TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from shopapp.forms import OrderForm
from shopapp.models import Item, Order, Tax, Discount
from mysite.settings import ROOT_URL
from app_users.models import Profile
from shopapp.mixins.payment_mixin import PaymentMixin


class SuccessPymentView(LoginRequiredMixin, TemplateView):
    login_url = 'app_users:login'
    template_name = 'shopapp/success_payment.html'


class ItemListView(ListView):
    model = Item


class ItemDetailView(DetailView):
    model = Item
    context_object_name = 'item'
    template_name = 'shopapp/item_detail.html'
    pk_url_kwarg = 'id'


class OrderDetailView(LoginRequiredMixin, DetailView):
    login_url = 'app_users:login'
    model = Order
    queryset = Order.objects.prefetch_related('items').prefetch_related('tax').prefetch_related('discount')
    context_object_name = 'order'
    template_name = 'shopapp/order_detail.html'
    pk_url_kwarg = 'id'


class OrderCreateView(LoginRequiredMixin, PaymentMixin, View):
    login_url = 'app_users:login'

    root_url = ROOT_URL
    page_after_add_payment_method = 'shopapp:item_list'
    success_payment_url = 'shopapp:success'

    def get(self, request: HttpRequest) -> HttpResponse:
        profile = Profile.objects.select_related('user').get(user=request.user)

        self.get_pyment_methods(profile.customer_id)

        template_name = 'shopapp/order_form.html'

        form = OrderForm()

        context = {
            'form': form
        }

        return render(request, template_name, context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = OrderForm(request.POST)

        if form.is_valid():
            form.instance.user = self.request.user
            items = form.cleaned_data['items'].all()

            # Set random tax and discount
            tax_value = random.choice(range(55))
            discount_value = random.choice(range(55))

            tax = Tax.objects.get_or_create(
                value=tax_value
            )

            discount = Discount.objects.get_or_create(
                value=discount_value
            )

            form.instance.tax = tax[0]
            form.instance.discount = discount[0]

            form.instance.total_price_cent = self._get_total_price(items)

            order = form.save()

            return redirect(reverse('shopapp:confirm_payment', kwargs={'type': 'order', 'id': order.id}))

    @staticmethod
    def _get_total_price(items):
        total_price = 0

        for item in items:
            total_price += item.price_cent

        return total_price


class ItemPymentView(LoginRequiredMixin, PaymentMixin, View):
    login_url = 'app_users:login'

    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        item_id = kwargs.get('id')
        item = Item.objects.get(id=item_id)

        profile = Profile.objects.select_related('user').get(user=request.user)

        payment_methods = self.get_pyment_methods(profile.customer_id)

        if payment_methods:
            return self.make_payment(
                amount=item.price_cent,
                customer=profile.customer_id,
                payment_method=payment_methods[0]['id']
            )

        else:
            return redirect(
                reverse(
                    'app_users:card'
                ) + '?next=' + reverse('shopapp:item_buy', args=[item_id])
            )


class PaymentConfirmView(LoginRequiredMixin, PaymentMixin, View):
    login_url = 'app_users:login'

    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        template_name = 'shopapp/confirm_payment.html'

        # Object attributes
        type_ = kwargs.get('type')
        id_ = kwargs.get('id')

        if type_ == 'order':
            obj = Order.objects. \
                prefetch_related('items'). \
                prefetch_related('tax'). \
                prefetch_related('discount'). \
                filter(id=id_).first()

            tax_perc = obj.tax.value  # Task %
            discount_perc = obj.discount.value  # Discount %

            _, total_amount_usd, discount_value_usd, tax_value_usd = self.__get_price_tuple(
                obj.total_price_cent,
                discount_perc,
                tax_perc
            )

        elif type_ == 'item':
            obj = Item.objects.filter(id=id_)
            tax_value_usd = 0
            discount_value_usd = 0
            total_amount_usd = 0

        else:
            raise ValueError(f'Wrong type: {type_}')

        context = {
            'id': id_,
            'type': type_,
            'object': obj,
            'total_amount': total_amount_usd,
            'tax': tax_value_usd,
            'discount': discount_value_usd,
        }

        return render(request, template_name, context)

    def post(self, request: HttpRequest, **kwargs) -> HttpResponse:
        # Object attributes
        type_ = kwargs.get('type')
        id_ = kwargs.get('id')

        if type_ == 'order':
            obj = Order.objects. \
                prefetch_related('items'). \
                prefetch_related('tax'). \
                prefetch_related('discount'). \
                filter(id=id_).first()

            tax_perc = obj.tax.value  # Task %
            discount_perc = obj.discount.value  # Discount %

            total_amount_cent, _, _, _ = self.__get_price_tuple(
                obj.total_price_cent,
                discount_perc,
                tax_perc
            )

            amount = total_amount_cent

        elif type_ == 'item':
            obj = Item.objects.filter(id=id_).first()
            amount = obj.price_cent

        else:
            raise ValueError(f'Wrong type: {type_}')

        profile = Profile.objects.select_related('user').get(user=self.request.user)

        payment_methods = self.get_pyment_methods(profile.customer_id)

        if payment_methods is None:
            return redirect(
                reverse(
                    'app_users:card'
                ) + '?next=' + reverse('shopapp:confirm_payment', kwargs={'type': type_, 'id': id_})
            )

        payment_method_card_id = payment_methods[0]['id']

        return self.make_payment(
            payment_method=payment_method_card_id,
            amount=amount,
            customer=profile.customer_id
        )

    @staticmethod
    def __get_price_tuple(start_price, discount=0, tax=0) -> Tuple[int, float, float, float]:
        """
        :return: Tuple of:
        - total_amount_cent - in cents
        - total_amount_usd - in USD
        - discount_value_usd - in USD
        - tax_value_usd - in USD
        """
        discount_value_cent = (start_price / 100) * discount  # In cents
        tax_value_cent = (start_price / 100) * tax  # In cents
        total_amount_cent = start_price - discount_value_cent + tax_value_cent  # In cents

        total_amount_usd = round(total_amount_cent / 100, 2)  # In $USD
        discount_value_usd = round(discount_value_cent / 100, 2)  # In $USD
        tax_value_usd = round(tax_value_cent / 100, 2)  # In $USD

        return int(total_amount_cent), total_amount_usd, discount_value_usd, tax_value_usd
