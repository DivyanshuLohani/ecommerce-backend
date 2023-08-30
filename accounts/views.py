from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import VendorSerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class CreateVendorView(CreateAPIView):

    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]

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
