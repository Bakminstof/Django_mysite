from django.urls import path

from shopapp.views import (
    ItemListView,
    ItemDetailView,
    ItemPymentView,
    OrderCreateView,
    OrderDetailView,
    PaymentConfirmView,
    SuccessPymentView,
)

app_name = 'shopapp'

urlpatterns = [
    # Items URLs
    path('items/', ItemListView.as_view(), name='item_list'),
    path('items/<int:id>/', ItemDetailView.as_view(), name='item_detail'),
    path('items/<int:id>/buy/', ItemPymentView.as_view(), name='item_buy'),
    # path('buy/<int:id>/', ItemPymentView.as_view(), name='item_buy'),  # If you like this path
    # Orders URLs
    path('orders/create/', OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:id>/', OrderDetailView.as_view(), name='order_detail'),
    # Payments URLs
    path('confirm_payment/<str:type>/<int:id>/', PaymentConfirmView.as_view(), name='confirm_payment'),
    path('success/', SuccessPymentView.as_view(), name='success'),
]
