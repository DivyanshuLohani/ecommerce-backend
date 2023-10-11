from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin
from .models import Product, Category
from rest_framework.permissions import AllowAny
from .serializers import ProductSerializer


class ProductView(GenericAPIView, RetrieveModelMixin):
    serializer_class = ProductSerializer
    lookup_field = 'uid'
    permission_classes = [AllowAny]

    def get_queryset(self):
        uid = self.kwargs[self.lookup_field]
        product = Product.objects.filter(uid=uid, status="publish")
        return product

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CategoryView(ListAPIView, RetrieveModelMixin):

    permission_classes = [AllowAny]

    serializer_class = ProductSerializer
    lookup_url_kwarg = None
    lookup_field = "slug"

    def get_queryset(self):
        slug = self.kwargs[self.lookup_field]
        products = Product.objects.filter(
            category__slug=slug, status="publish")
        return products


class ProductSearch(ListAPIView, RetrieveModelMixin):
    paginate_by = 20
    serializer_class = ProductSerializer

    permission_classes = [AllowAny]

    def get_queryset(self):
        search = self.kwargs['search']

        if not search:
            return Product.objects.none()
        mx_price = self.request.GET.get("mx_price")
        mi_price = self.request.GET.get("mi_price")
        query_dict = {
            "name__icontains": search
        }
        if mx_price and mi_price:
            query_dict['price__lte'] = mx_price
            query_dict['price__gte'] = mi_price

        return Product.objects.filter(**query_dict, status="publish")
