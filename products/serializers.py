from rest_framework import serializers

from .models import Category, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "uid",
            "name",
            "description",
            "price",
            "image",
            "og_price",
            "in_stock",
            "digital"
        )


class CategorySerializer(serializers.ModelSerializer):
    # products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "products",
            "slug",
        )
