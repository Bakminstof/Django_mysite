import stripe

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.views import View
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import (
    LoginView as DjangoLoginView,
    LogoutView as DjangoLogoutView
)

from app_users.forms import ExtendUserCreationForm, CardForm
from app_users.models import Profile


class LoginView(DjangoLoginView):
    template_name = 'app_users/registration/login.html'


class LogoutView(DjangoLogoutView):
    template_name = 'app_users/registration/logout.html'


class AccountView(LoginRequiredMixin, View):
    login_url = 'app_users:login'

    @staticmethod
    def get(request: HttpRequest) -> HttpResponse:
        template_name = 'app_users/account.html'

        profile = Profile.objects.select_related('user').get(user=request.user)

        payment_methods = stripe.Customer.list_payment_methods(
            profile.customer_id,
            type="card",
        )

        if payment_methods['data']:
            last4 = payment_methods['data'][0]['card']['last4']
        else:
            last4 = None

        context = {
            'last4': last4,
            'profile': profile,
        }

        return render(request, template_name, context)


class CardView(LoginRequiredMixin, View):
    login_url = 'app_users:login'

    @staticmethod
    def get(request: HttpRequest) -> HttpResponse:
        template_name = 'app_users/card_form.html'

        profile = Profile.objects.select_related('user').get(user=request.user)

        payment_methods = stripe.Customer.list_payment_methods(
            profile.customer_id,
            type="card",
        )

        if payment_methods['data']:
            card = payment_methods['data'][0]['card']
        else:
            card = None

        form = CardForm()

        context = {
            'form': form,
            'card': card,
            'next_page': request.GET.get('next')
        }

        return render(request, template_name, context)

    @staticmethod
    def post(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        profile = Profile.objects.select_related('user').get(user=request.user)

        form = CardForm(request.POST)

        if form.is_valid():
            payment_method = stripe.PaymentMethod.create(
                type="card",
                card={
                    'number': form.cleaned_data['number'],
                    'exp_month': form.cleaned_data['exp_month'],
                    'exp_year': form.cleaned_data['exp_year'],
                    'cvc': form.cleaned_data['cvc'],
                },
            )

            stripe.PaymentMethod.attach(
                payment_method.id,
                customer=profile.customer_id,
            )

            if request.POST.get('next_page'):
                return redirect(request.POST.get('next_page'))

            else:
                return redirect(reverse('app_users:account'))

    def patch(self):  # TODO update card
        return redirect(reverse('app_users:account'))

    def delete(self):  # TODO delete card
        return redirect(reverse('app_users:account'))


class RegisterView(View):
    @staticmethod
    def get(request: HttpRequest) -> HttpResponse:
        template_name = 'app_users/registration/register.html'

        auth_form = ExtendUserCreationForm()

        context = {
            'form': auth_form
        }

        return render(request, template_name, context)

    @staticmethod
    def post(request: HttpRequest) -> HttpResponse:
        register_form = ExtendUserCreationForm(request.POST)

        if register_form.is_valid():
            register_form.save()

            username = register_form.cleaned_data['username']
            raw_password = register_form.cleaned_data['password1']
            city = register_form.cleaned_data.get('city', None)
            phone = register_form.cleaned_data.get('phone', None)
            email = register_form.cleaned_data.get('email', None)

            user = authenticate(username=username, password=raw_password)
            login(request, user)

            customer = stripe.Customer.create(
                name=username,
                email=email,
                phone=phone,
                address={'city': city} if city else None
            )

            Profile.objects.create(
                user=user,
                city=city,
                phone=phone,
                customer_id=customer.id
            )

            return redirect(reverse('app_users:account'))

        else:
            context = {
                'form': register_form,
                'error': 'Incorrect data has been entered or a user with such a nickname has already been registered'
            }

            return render(request, 'app_users/registration/register.html', context=context)
