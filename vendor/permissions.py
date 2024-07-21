
from rest_framework import permissions


class IsVendor(permissions.BasePermission):
    """
    Check for vendor account before performing actions
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return bool(request.user.vendor.first())
