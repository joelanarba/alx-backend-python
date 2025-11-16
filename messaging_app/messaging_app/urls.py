#!/usr/bin/env python3
"""Main urls for messaging_app"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("chats.urls")),  # ensures /api/ prefix for all endpoints
]
