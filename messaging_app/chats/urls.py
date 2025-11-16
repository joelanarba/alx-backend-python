#!/usr/bin/env python3
"""URLs for chats app using DRF DefaultRouter"""

from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

# Create router and register viewsets
router = routers.DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")
router.register(r"messages", MessageViewSet, basename="message")

# Include router-generated URLs
urlpatterns = [
    path("", include(router.urls)),
]
