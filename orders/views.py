from rest_framework.generics import (
    CreateAPIView, DestroyAPIView,
    get_object_or_404,
    ListAPIView
)
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from .models import CartItem, Product, Order, Address, OrderItem
from .serializers import CartItemSerializer, OrderSerializer, OrderObjectSerializer, PaymentVerifySerializer, CartItemViewSerializer
from products.serializers import ProductSerializer
from django.conf import settings

# Create your views here.


class GetCartView(ListAPIView):

    serializer_class = CartItemViewSerializer

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user).all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CartView(CreateAPIView):

    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        proudct = Product.objects.filter(
            uid=serializer.validated_data.get("product")
        ).first()
        quantity = serializer.validated_data.get("quantity")
        # Delete Item

        cart_obj = CartItem.objects.filter(
            product=proudct,
            user=self.request.user
        ).first()

        if cart_obj:
            cart_obj.quantity = quantity
            return cart_obj.save()
        else:
            return serializer.save(user=self.request.user, product=proudct)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        items = CartItem.objects.filter(user=self.request.user).all()
        serializer = CartItemViewSerializer(items, many=True)
        return Response(serializer.data, status=201, headers=headers)


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
            payment_method = serializer.validated_data['payment_method']
            order = Order(user=request.user, address=address,
                          payment_method=payment_method)
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

            # TODO: send email to user reguarding the order status

            if payment_method == "rzp":
                rzp_data = {
                    "amount": float(order.total) * 100,
                    "currency": "INR",
                    # "receipt": "receipt#1",
                    # "notes": {
                    #     "key1": "value3",
                    #     "key2": "value2"
                    # }
                }
                # TODO: ADD ERROR HANDLING
                resp = settings.RZP_CLIENT.order.create(data=rzp_data)
                order.payment_order_id = resp['id']
                order.status = "payment_pending"
                order.save()

            order_serializer = OrderObjectSerializer(order)
            return Response(order_serializer.data, HTTP_201_CREATED)

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
            return Order.objects.filter(user=self.request.user, uid=order_id, status="confirm")

        return Order.objects.filter(user=self.request.user)


class OrderPaymentVerify(APIView):

    def post(self, request, uid):
        serializer = PaymentVerifySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            order = get_object_or_404(Order, uid=uid)
            signature = settings.RZP_CLIENT.utility.verify_payment_signature({
                'razorpay_order_id': order.payment_order_id,
                'razorpay_payment_id': serializer.validated_data['payment_id'],
                'razorpay_signature': serializer.validated_data['payment_signature']
            })
            if signature:
                order.status = "confirm"
                order.save()
                return Response({"message": "Success"})
            else:
                raise ParseError("Signature doesn't match")

        raise ParseError(serializer.errors)
