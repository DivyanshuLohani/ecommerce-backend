from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin
from .models import Product, Category
from .serializers import ProductSerializer


class ProductView(GenericAPIView, RetrieveModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'


class ProductCreateView(GenericAPIView, CreateModelMixin):
    serializer_class = ProductSerializer


class CategoryView(ListAPIView, RetrieveModelMixin):

    serializer_class = ProductSerializer
    lookup_url_kwarg = None
    lookup_field = "slug"

    def get_queryset(self):
        slug = self.kwargs[self.lookup_field]
        products = Product.objects.filter(category__slug=slug)
        return products
