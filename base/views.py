from django.shortcuts import render
from django.views.generic import View
from django.contrib import messages
from products.models import Category
# Create your views here.


class HomePage(View):
    def get(self, request):
        featured_cat = Category.objects.filter(parent=None)[:4]
        return render(
            request,
            "base/index.html",
            {
                "featured_cat": featured_cat
            }
        )
