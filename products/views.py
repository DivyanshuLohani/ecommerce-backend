from rest_framework.generics import (
    ListAPIView,
    GenericAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    get_object_or_404
)
from rest_framework.exceptions import ParseError
from rest_framework.mixins import RetrieveModelMixin
from .models import Banner, Product, Category, ProductReview
from rest_framework.permissions import AllowAny
from .serializers import BannerSerializer, CategorySerializer, ProductSerializer, ProductReviewSerializer


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


class ReviewCreateView(CreateAPIView):
    serializer_class = ProductReviewSerializer

    def perform_create(self, serializer):
        product = Product.objects.filter(uid=self.kwargs['uid']).first()
        if not product:
            raise ParseError("Bad product ID")

        serializer.save(product=product, user=self.request.user)


class ReviewSeeView(ListAPIView, RetrieveModelMixin):
    serializer_class = ProductReviewSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return ProductReview.objects.filter(product__uid=self.kwargs['uid'])


class ReviewAddDeleteUpdateView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductReviewSerializer
    lookup_field = "uid"
    lookup_url_kwarg = "r_uid"
    queryset = ProductReview.objects.all()

    def check_object_permissions(self, request, obj):
        return request.user == obj.user


class BannerListView(ListAPIView, CreateAPIView):
    queryset = Banner.objects.filter(is_active=True)
    serializer_class = BannerSerializer
    permission_classes = [AllowAny]


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
