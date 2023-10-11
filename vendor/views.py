from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from accounts.serializers import VendorSerializer
from products.serializers import ProductSerializer, ProductImageSerializer
from products.models import Category, Product, ProductImage
from .permissions import IsVendor


class ProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsVendor]
    serializer_class = VendorSerializer

    def get_object(self):

        return self.request.user.vendor.first()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class AddProductView(CreateAPIView):
    permission_classes = [IsVendor]
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        category = Category.objects.filter(
            slug=request.data.get("category")
        ).first()
        if not category:
            return Response(
                {"message": "Invalid Category"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(vendor=request.user.vendor.first(), category=category)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProductsView(ListAPIView, RetrieveModelMixin):

    serializer_class = ProductSerializer
    lookup_url_kwarg = None

    def get_queryset(self):
        products = Product.objects.filter(
            vendor=self.request.user.vendor.first()
        )
        return products


class ProductDetailView(RetrieveUpdateAPIView):
    permission_classes = [IsVendor]
    serializer_class = ProductSerializer

    def get_object(self):
        uid = self.kwargs['product_id']
        p = Product.objects.filter(uid=uid).first()
        if not p or p.vendor != self.request.user.vendor.first():
            raise PermissionDenied("You cannot access that object")
        return p


class ProductImageView(CreateAPIView, DestroyAPIView):
    permission_classes = [IsVendor]
    serializer_class = ProductSerializer
    lookup_field = 'uid'
    queryset = ProductImage.objects.all()

    def create(self, request, *args, **kwargs):
        product = Product.objects.filter(uid=self.kwargs['product_id']).first()
        if not product:
            return Response(
                {"message": "Invalid Category"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ProductImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product)

        product = Product.objects.filter(uid=self.kwargs['product_id']).first()
        serializer = ProductSerializer(product)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
