from django.urls import path, include
from django.conf import settings
from .views import CreateVendorView, AddressView, AddressUpdate, GoogleOAuth2, FacebookOauth

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    # path('', include('djoser.social.urls')),
    path('google/', GoogleOAuth2.as_view()),
    path('facebook/', FacebookOauth.as_view()),
    path('vendor/', CreateVendorView.as_view()),
    path('addresses/', AddressView.as_view()),
    path('address/<str:uid>/', AddressUpdate.as_view()),
]
