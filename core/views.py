from django.shortcuts import render

from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import VendorGroupChatMessage,Producer,Rating
from .serializers import (
    VendorGroupChatMessageSerializer,ProducerSerializer,ProducerDetailSerializer
    ,ProducerReviewSerializer,RatingCreateSerializer)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Vendor  # adjust import path if needed
from django.contrib.auth import authenticate, get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from .models import ChatMessage
from .serializers import SignupSerializer, LoginSerializer, ChatMessageSerializer
from django.db.models import Q
from .serializers import ChatMessageSerializer
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny

User = get_user_model()

class VendorGroupChatListCreateAPIView(generics.ListCreateAPIView):
    queryset = VendorGroupChatMessage.objects.all().order_by('timestamp')
    serializer_class = VendorGroupChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'vendor':
            raise PermissionDenied("Only vendors can send group chat messages.")
        try:
            vendor = Vendor.objects.get(user=user)
        except Vendor.DoesNotExist:
            raise PermissionDenied("Vendor profile not found.")
        serializer.save(vendor=vendor)
class VendorProducerListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Only check if user is logged in

    def get(self, request):
        user = request.user

        # Inline vendor permission check
        if not hasattr(user, 'vendor'):
            return Response({'detail': 'Only vendors can access this resource.'}, status=status.HTTP_403_FORBIDDEN)

        producers = Producer.objects.all()
        serializer = ProducerSerializer(producers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class ProducerDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, producer_id):
        user = request.user

        # Only vendors or admins can access
        if user.role not in ['vendor', 'admin']:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            producer = Producer.objects.get(id=producer_id)
        except Producer.DoesNotExist:
            return Response({'detail': 'Producer not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProducerDetailSerializer(producer)
        return Response(serializer.data, status=status.HTTP_200_OK)
class ProducerOwnReviewsAPIView(generics.ListAPIView):
    serializer_class = ProducerReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role != 'producer':
            raise PermissionDenied("Only producers can view their reviews.")

        producer = Producer.objects.get(user=user)
        return Rating.objects.filter(producer=producer).select_related('vendor__user')
class SubmitRatingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        if not hasattr(user, 'vendor'):
            return Response({"detail": "Only vendors can submit ratings."}, status=403)

        serializer = RatingCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            rating = serializer.save()
            return Response({"detail": "Rating submitted successfully."}, status=201)
        return Response(serializer.errors, status=400)
    
class SignupView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user)
            return Response({"message": "User created", "token": token.key}, status=201)
        return Response(serializer.errors, status=400)

# Login
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"message": "Login successful", "token": token.key})
            return Response({"error": "Invalid credentials"}, status=401)
        return Response(serializer.errors, status=400)

# Logout
class LogoutView(APIView):
    #permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully"}, status=200)

# Send Message
class ChatMessageCreateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sender = request.user
        receiver_id = request.data.get('receiver')
        message = request.data.get('message')

        if not receiver_id or not message:
            return Response({'error': 'Receiver and message are required'}, status=400)

        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return Response({'error': 'Receiver not found'}, status=404)

        chat_message = ChatMessage.objects.create(sender=sender, receiver=receiver, message=message)
        serializer = ChatMessageSerializer(chat_message)
        return Response(serializer.data, status=201)

# Get Conversation
class ChatMessageListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        current_user = request.user
        try:
            other_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        messages = ChatMessage.objects.filter(
            Q(sender=current_user, receiver=other_user) |
            Q(sender=other_user, receiver=current_user)
        ).order_by('timestamp')

        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)

class SentMessagesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        sent_messages = ChatMessage.objects.filter(sender=user).order_by('-timestamp')
        serializer = ChatMessageSerializer(sent_messages, many=True)
        return Response(serializer.data)


class AllUserMessagesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Fetch both sent and received messages
        messages = ChatMessage.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).order_by('timestamp')

        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)