#!/usr/bin/env python3
"""URLs for chats app using DRF NestedDefaultRouter"""

from django.urls import path, include
from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet

# Main router for conversations
router = routers.DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")

# Nested router for messages under conversations
conversation_router = routers.NestedDefaultRouter(router, r"conversations", lookup="conversation")
conversation_router.register(r"messages", MessageViewSet, basename="conversation-messages")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(conversation_router.urls)),
]
