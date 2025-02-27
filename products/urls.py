from django.contrib import admin
from django.urls import path, include
from .views import BannerListView, ProductView, CategoryView, ProductSearch, ReviewCreateView, ReviewAddDeleteUpdateView, ReviewSeeView, CategoryListView
from django.views import View
from rest_framework.response import Response


urlpatterns = [
    path('banners/', BannerListView.as_view(), name='banner-list'),
    path('categories/', CategoryListView.as_view()),
    path('<str:uid>/', ProductView.as_view()),
    path('<str:uid>/reviews/', ReviewCreateView.as_view()),
    path('<str:uid>/reviews/get/', ReviewSeeView.as_view()),
    path('<str:uid>/reviews/<str:r_uid>/', ReviewAddDeleteUpdateView.as_view()),
    path('category/<str:slug>/', CategoryView.as_view()),
    path('search/<str:search>/', ProductSearch.as_view()),
]
