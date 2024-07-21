from django.contrib import admin
from .models import Vendor, Address, User
# Register your models here.

admin.site.register(Vendor)
admin.site.register(Address)
admin.site.register(User)
