from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.throttling import UserRateThrottle
from .models import FriendRequest
from .serializers import UserSerializer, UserSignupSerializer, UserLoginSerializer, FriendRequestSerializer
class SignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.save()
        return Response({
            'email': user_data['email'],
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
            'message': "user created succesfully",
            'auth_token': user_data['token']
        })

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        return Response({'auth_token': token, "message":"user login succesfully"})

class SearchUserView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        return User.objects.filter(
            Q(email__iexact=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SendFriendRequestThrottle(UserRateThrottle):
    rate = '3/minute'


class SendFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [SendFriendRequestThrottle]

    def post(self, request, *args, **kwargs):
        to_user_id = request.data.get('to_user_id')
        to_user = User.objects.get(id=to_user_id)

        if request.user == to_user:
            return Response({'status': 'You cannot send a friend request to yourself.'},
                            status=status.HTTP_400_BAD_REQUEST)

        friend_request, created = FriendRequest.objects.get_or_create(
            from_user=request.user,
            to_user=to_user
        )
        if created:
            return Response({'status': 'Friend request sent.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'Friend request already sent.'}, status=status.HTTP_200_OK)


class AcceptFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request_id = request.data.get('request_id')
        try:
            friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user)
        except FriendRequest.DoesNotExist:
            return Response({'status': 'Friend request not found or not for the current user.'},
                            status=status.HTTP_404_NOT_FOUND)

        friend_request.accepted = True
        friend_request.save()
        return Response({'status': 'Friend request accepted.'}, status=status.HTTP_200_OK)


class RejectFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request_id = request.data.get('request_id')
        try:
            friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user)
        except FriendRequest.DoesNotExist:
            return Response({'status': 'Friend request not found or not for the current user.'},
                            status=status.HTTP_404_NOT_FOUND)

        friend_request.delete()
        return Response({'status': 'Friend request rejected.'}, status=status.HTTP_200_OK)


class ListFriendsView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friends = User.objects.filter(
            Q(sent_requests__to_user=user, sent_requests__accepted=True) |
            Q(received_requests__from_user=user, received_requests__accepted=True)
        ).distinct()
        return friends


class ListPendingRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(to_user=user, accepted=False)