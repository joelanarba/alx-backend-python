#!/usr/bin/env python3
"""URLs for chats API"""

from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

# Use DefaultRouter as required
router = routers.DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")
router.register(r"messages", MessageViewSet, basename="message")

urlpatterns = [
    path("", include(router.urls)),  # router-generated routes included here
]
