from django.urls import path
from .views import ProfileView, AddProductView, ProductsView, ProductDetailView, ProductImageView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name="vendor_profile"),
    path('product/add/', AddProductView.as_view(), name="vendor_add_product"),
    path('products/', ProductsView.as_view(), name="vendor_products"),
    path('product/<str:product_id>/', ProductDetailView.as_view(),
         name="vendor_product_detail"),
    path('product/<str:product_id>/image/', ProductImageView.as_view(),
         name="vendor_product_image"),
    path('product/<str:product_id>/image/<str:uid>/', ProductImageView.as_view(),
         name="vendor_product_image"),

]
