from django.contrib import admin
from .models import Banner, Category, Product, ProductImage

# Register your models here.
admin.site.register([Category, Product, ProductImage, Banner])
