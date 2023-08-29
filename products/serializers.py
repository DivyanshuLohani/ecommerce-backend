from rest_framework import serializers
from accounts.serializers import VendorSerializer, Vendor
from .models import Category, Product


class VendorSnippetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        exclude = ["id", "user", "contact", "address"]


class CategorySerializer(serializers.ModelSerializer):
    # products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "uid",
            "name",
            "description",
            "slug",
            "image",
        )


class ProductSerializer(serializers.ModelSerializer):

    vendor = VendorSnippetSerializer(read_only=True)
    category = CategorySerializer()
    images = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Product
        # fields = (
        #     "uid",
        #     "name",
        #     "description",
        #     "price",
        #     "og_price",
        #     "image",
        #     "status",
        #     "in_stock",
        #     "digital",
        # )
        # fields = "__all__"
        exclude = ["id"]
