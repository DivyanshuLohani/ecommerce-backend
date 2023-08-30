from django.urls import path, include
from django.conf import settings
from .views import CreateVendorView, AddressView, AddressUpdate

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('vendor/', CreateVendorView.as_view()),
    path('addresses/', AddressView.as_view()),
    path('address/<str:uid>/', AddressUpdate.as_view()),
]
