from rest_framework import serializers
from accounts.serializers import Vendor, UserProfileSerializer
from .models import Category, Product, ProductImage, ProductReview


class VendorSnippetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        exclude = ["user", "contact", "address"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ["parent"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ['product']


class ProductSerializer(serializers.ModelSerializer):

    vendor = VendorSnippetSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product

        fields = "__all__"

    def validate_category(self, value):
        if isinstance(value, str):
            c = Category.objects.filter(slug=value).exists()
            if not c:
                raise serializers.ValidationError("Category doesn't exist")
            return value
        raise serializers.ValidationError("Category is invalid")


class ProductReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductReview
        exclude = ['product']

    user = UserProfileSerializer()
