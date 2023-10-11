from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import VendorSerializer, AddressSerializer
from .models import Address
# Create your views here.


class CreateVendorView(CreateAPIView):

    serializer_class = VendorSerializer

    def create(self, request, *args, **kwargs):
        if request.user.vendor.first():
            return Response(
                {"error": "Already vendor account exists with your account"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = VendorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AddressView(CreateAPIView, ListAPIView):

    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):

        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AddressUpdate(RetrieveUpdateDestroyAPIView):

    serializer_class = AddressSerializer
    lookup_field = "uid"
    lookup_url_kwarg = "uid"

    def get_queryset(self):
        uid = self.kwargs['uid']
        return Address.objects.filter(user=self.request.user, uid=uid)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
