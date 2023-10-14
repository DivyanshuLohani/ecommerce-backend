from rest_framework.generics import (
    CreateAPIView, DestroyAPIView,
    get_object_or_404,
    ListAPIView, RetrieveAPIView
)
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from .models import CartItem, Product, Order, Address, OrderItem
from .serializers import CartItemSerializer, OrderSerializer, OrderObjectSerializer

# Create your views here.


class CartView(CreateAPIView):

    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        proudct = Product.objects.filter(
            uid=serializer.validated_data.get("product")
        ).first()
        cart_obj = CartItem.objects.filter(
            product=proudct,
            user=self.request.user
        ).first()
        if cart_obj:
            cart_obj.quantity = serializer.validated_data.get("quantity")
            return cart_obj.save()
        else:
            return serializer.save(user=self.request.user, product=proudct)


class Checkout(APIView):

    def post(self, request):
        cart_items = CartItem.objects.filter(user=request.user).all()
        if not cart_items:
            raise ParseError("Cannot make an empty order")
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            address = Address.objects.filter(
                uid=serializer.validated_data['address']
            ).first()
            if not address or (address and (address.user != self.request.user)):
                raise NotFound("Address doesn't exist")

            order = Order(user=request.user, address=address)
            order.save()
            order_items = [
                OrderItem(
                    order=order, product=item.product, quantity=item.quantity
                )
                for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)

            cart_items.delete()

            # Order Created sussfully send return response
            order_serializer = OrderObjectSerializer(order)
            return Response(order_serializer.data, HTTP_201_CREATED)

            # TODO: send email to user reguarding the order status
            # TODO: add system for payment integration

        else:
            raise ParseError(serializer.errors)


class CartDelete(DestroyAPIView):

    lookup_field = "uid"

    def get_object(self):
        product_uid = self.kwargs.get(self.lookup_field)
        return get_object_or_404(
            CartItem, user=self.request.user,
            product__uid=product_uid
        )


class AccountOrders(ListAPIView):

    serializer_class = OrderObjectSerializer

    def get_queryset(self):
        order_id = self.kwargs.get("uid")
        if order_id:
            return Order.objects.filter(user=self.request.user, uid=order_id)

        return Order.objects.filter(user=self.request.user)
