from django.contrib import admin
from django.urls import path, include
from .views import ProductView, CategoryView, ProductSearch
from django.views import View
from rest_framework.response import Response


urlpatterns = [
    path('<str:uid>/', ProductView.as_view()),
    path('category/<str:slug>/', CategoryView.as_view()),
    path('search/<str:search>/', ProductSearch.as_view()),
]
