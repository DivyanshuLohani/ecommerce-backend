from django.urls import path
from .views import CartView, Checkout, CartDelete, AccountOrders, GetCartView, OrderPaymentVerify

urlpatterns = [
    path('cart/', CartView.as_view(), name="cart"),
    path('cart/view/', GetCartView.as_view(), name="view_cart"),
    path('cart/<str:uid>/delete/', CartDelete.as_view(), name="cart_delete"),
    path('checkout/', Checkout.as_view(), name="checkout"),
    path('orders/', AccountOrders.as_view(), name="orders"),
    path('orders/<str:uid>/', AccountOrders.as_view(), name="order_item"),
    path('orders/<str:uid>/verify_payment/',
         OrderPaymentVerify.as_view(), name="payment_verify"),
]
