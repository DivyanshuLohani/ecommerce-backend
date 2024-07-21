from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.conf import settings
from .views import HomePage

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("about/", lambda r: render(r, "base/index.html"), name="about"),
]
