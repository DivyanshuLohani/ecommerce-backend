from rest_framework import serializers
from accounts.serializers import VendorSerializer, Vendor
from .models import Category, Product, ProductImage


class VendorSnippetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        exclude = ["id", "user", "contact", "address"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ["id", "parent"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ['id', 'product']


class ProductSerializer(serializers.ModelSerializer):

    vendor = VendorSnippetSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

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

    def validate_category(self, value):
        if isinstance(value, str):
            c = Category.objects.filter(slug=value).exists()
            if not c:
                raise serializers.ValidationError("Category is invalid")
            return value
        raise serializers.ValidationError("Category is invalid")
