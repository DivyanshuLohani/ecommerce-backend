from base.models import BaseModel
from products.models import Product
from django.db import models
from accounts.models import User, Address

ORDER_STATUS_CHOICES = (
    ("process", "Processing"),
    ("payment_pending", "Payment Pending"),
    ("confirm", "Confrimed"),
    ("ship", "Shipped"),
    ("diliver", "Delivered")
)

PAYMENT_CHOICES = (
    ("cod", "Pay On Delivery"),
    ("paypal", "Paypal"),
    ("rzp", "Razor Pay")
)


class Order(BaseModel):

    status = models.CharField(
        choices=ORDER_STATUS_CHOICES,
        default=ORDER_STATUS_CHOICES[0][0],
        max_length=15
    )

    payment_order_id = models.CharField(
        default=None,
        null=True,
        max_length=512
    )

    payment_method = models.CharField(
        choices=PAYMENT_CHOICES,
        default=PAYMENT_CHOICES[0][0],
        max_length=20,
    )

    user = models.ForeignKey(
        User, related_name="orders",
        on_delete=models.SET_NULL,
        null=True
    )
    address = models.ForeignKey(
        Address, related_name="orders",
        on_delete=models.SET_NULL,
        null=True
    )

    @property
    def total(self):
        return sum([x.product.price for x in self.items.all()])

    @property
    def og_total(self):
        return sum([x.product.og_price for x in self.items.all()])

    @property
    def discount(self):
        return sum([x.product.discount for x in self.items.all()])


class OrderItem(BaseModel):
    order = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="orders", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def price(self):
        return self.product.price * self.quantity


class CartItem(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def price(self):
        return self.product.price * self.quantity
