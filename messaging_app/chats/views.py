#!/usr/bin/env python3
"""API views for chats app"""

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for listing and creating conversations"""

    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["participants__email"]

    @action(detail=True, methods=["post"])
    def add_message(self, request, pk=None):
        """Send a message to this conversation"""
        conversation = self.get_object()
        serializer = MessageSerializer(
            data={
                **request.data,
                "conversation": str(conversation.conversation_id)
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for listing and creating messages"""

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["sender__email", "message_body"]
