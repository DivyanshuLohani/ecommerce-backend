from django.urls import path, include
from django.conf import settings
from .views import CreateVendorView

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('vendor/', CreateVendorView.as_view()),
]
