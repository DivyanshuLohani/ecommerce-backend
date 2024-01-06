from rest_framework import serializers
from products.models import Product
from products.serializers import ProductSerializer
from .models import CartItem, Order
from accounts.models import Address
from accounts.serializers import AddressSerializer
from django.conf import settings


def razorpay_oid(instance):
    return {
        "key": settings.RZP_ID,
        "amount": f"{instance.total * 100}",
        "currency": "INR",
        "name": settings.SITE_NAME,
        "description": f"Your order on {settings.SITE_NAME}",
        "image": "https://example.com/your_logo",
        "order_id": f"{instance.payment_order_id}",
        # "callback_url": "https://eneqd3r9zrjok.x.pipedream.net/",
        "prefill": {
            "name": instance.user.get_full_name(),
            "email": instance.user.email,
            # "contact": "9000090000"
        },

        "theme": {
            "color": "#3399cc"
        }
    }


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

    product = serializers.CharField()

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "The quantity must be greater than 0."
            )
        return value


class CartItemViewSerializer(serializers.ModelSerializer):
    """
        View only serialzier this should only be used only to provide data to the user
        Not to write new items to the cart
    """
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

    product = ProductSerializer()


class OrderSerializer(serializers.Serializer):

    address = serializers.CharField()
    payment_method = serializers.CharField()


class PaymentVerifySerializer(serializers.Serializer):

    payment_id = serializers.CharField()
    payment_signature = serializers.CharField()


class OrderObjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        exclude = ['user']

    address = AddressSerializer()
    items = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()
    og_subtotal = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()

    payment_info = serializers.SerializerMethodField()

    def get_subtotal(self, instance):
        return instance.total

    def get_og_subtotal(self, instance):
        return instance.og_total

    def get_discount(self, instance):
        return instance.discount

    def get_items(self, instance):
        return ProductSerializer([i.product for i in instance.items.all()], many=True).data

    def get_payment_info(self, instance: Order):
        if instance.payment_order_id is None:
            return None
        return razorpay_oid(instance)
