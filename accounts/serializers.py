from rest_framework.serializers import ModelSerializer
from .models import Vendor, Address, User


class UserProfileSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class VendorSerializer(ModelSerializer):

    class Meta:
        model = Vendor
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'user': {'write_only': True}
        }


class AddressSerializer(ModelSerializer):

    class Meta:
        model = Address
        exclude = ["id", "user"]
        read_only_fields = []
