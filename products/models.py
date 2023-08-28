from django.db import models

# Create your models here.
import random
from typing import Iterable, Optional
from django.utils.text import slugify
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files import File
from accounts.models import Vendor
from shortuuidfield import ShortUUIDField
from base.models import BaseModel
import os


def product_upload(instance, filename):
    return f"media/{instance.category.uid}/{instance.uid}/{filename}"


def product_image(instance, filename):
    return f"media/{instance.product.category.uid}/{instance.product.uid}/{filename}"


def category_image(x, y): return f"media/{x.uid}/{y}"


def get_slug(klass, name):
    slug = slugify(name)
    if klass.objects.filter(slug=slug).exists():
        return get_slug(klass, slug+str(random.randint(1, 1000)))
    return slug


PRODUCT_STATUS_CHOICES = (
    ("review", "In Review"),
    ("publish", "Published"),
    ("disable", "Disabled"),
    ("draft", "Draft"),
    ("reject", "Rejected")
)


class Category(BaseModel):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "Category", on_delete=models.CASCADE, blank=True, default=None, null=True
    )
    slug = models.SlugField(blank=True, unique=True)
    description = models.CharField(max_length=1024, default="")
    image = models.ImageField(
        "Category Image",
        upload_to=category_image,
        default=None,
        null=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = get_slug(Category, self.name)

        super(Category, self).save(*args, **kwargs)


class Tags(BaseModel):
    name = models.CharField(max_length=128)

    class Meta:
        ordering = ["name"]


class Product(BaseModel):
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE
    )

    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to=product_upload, blank=True, null=True)

    price = models.DecimalField(max_digits=1000, decimal_places=2)
    og_price = models.DecimalField(
        "Orignal Price", max_digits=1000, decimal_places=2
    )

    specifications = models.TextField(null=True, blank=True)

    tags = models.ManyToManyField(Tags, max_length=5, default=None, blank=True)

    status = models.CharField(
        choices=PRODUCT_STATUS_CHOICES,
        default=PRODUCT_STATUS_CHOICES[0][0],
        max_length=20
    )

    in_stock = models.BooleanField(default=True)
    digital = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = get_slug(Product, self.name)
        if not (self.image or self.price or self.og_price):
            self.status = PRODUCT_STATUS_CHOICES[3][0]

        super(Product, self).save(*args, **kwargs)

    @property
    def discount(self):
        # Discount Formula
        return round((self.og_price - self.price / self.og_price) * 100, 0)

    def __str__(self):
        return self.name


class ProductImage(BaseModel):
    image = models.ImageField(upload_to=product_image)
    product = models.ForeignKey(
        Product,
        related_name="images",
        on_delete=models.CASCADE,
    )

# TODO: add Featured Product
# class FeaturedProduct(BaseModel):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     image = models.ImageField("Featured Image", upload_to=product_image)
