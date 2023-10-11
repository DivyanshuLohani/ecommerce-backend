from rest_framework import serializers
from products.models import Product
from products.serializers import ProductSerializer
from .models import CartItem, Order
from accounts.models import Address


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


class OrderSerializer(serializers.Serializer):

    address = serializers.CharField()
    payment_method = serializers.CharField()


class OrderConfrimSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        exclude = ['address', 'user', ]

    items = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()
    og_subtotal = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()

    def get_subtotal(self, instance):
        return instance.total

    def get_og_subtotal(self, instance):
        return instance.og_total

    def get_discount(self, instance):
        return instance.discount

    def get_items(self, instance):
        return ProductSerializer([i.product for i in instance.items.all()], many=True).data
