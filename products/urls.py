from django.contrib import admin
from django.urls import path, include
from .views import ProductView, CategoryView

urlpatterns = [
    path('get/<str:slug>/', ProductView.as_view()),
    path('category/<str:slug>/', CategoryView.as_view())
]
