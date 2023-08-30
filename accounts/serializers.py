from rest_framework.serializers import ModelSerializer
from .models import Vendor


class VendorSerializer(ModelSerializer):

    class Meta:
        model = Vendor
        exclude = ['id']
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'user': {'write_only': True}
        }
