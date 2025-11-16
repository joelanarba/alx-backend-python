#!/usr/bin/env python3
"""URLs for chats API"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")
router.register(r"messages", MessageViewSet, basename="message")

# The API URLs are now automatically determined by the router
urlpatterns = [
    path("", include(router.urls)),  # no 'api/' here, include it in project urls.py
]
