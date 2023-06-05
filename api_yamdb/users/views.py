from rest_framework.generics import GenericAPIView
from rest_framework import response, status
from . import serializers, models
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from .models import ConfirmationCode, CustomUser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsUser, IsAdministator, IsModerator, IsSuperUser, IsAnAuthor
from django.core.mail import send_mail
import uuid
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from .utils import get_confirmation_code


class SignUpView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.SignUpSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if CustomUser.objects.filter(username=data.get('username'), email=data.get('email')).exists():
            return Response(get_confirmation_code(data), status=status.HTTP_200_OK)
        serializer.is_valid(raise_exception=True)
        if data.get('username') == 'me':
            return Response({'error': 'Restricted'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(get_confirmation_code(serializer.validated_data), status=status.HTTP_200_OK)


class TokenView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.TokenSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        if not CustomUser.objects.filter(username=data.get('username')).exists():
            return Response({'error': 'Bad request'}, status=status.HTTP_404_NOT_FOUND)
        if not CustomUser.objects.filter(confirmation_code=data.get('confirmation_code')).exists():
            return Response({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(CustomUser, username=username)
        tokens = RefreshToken.for_user(user).access_token
        return Response({'token': str(tokens)}, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    search_field = ('$username', )

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsAdministator, ]
        if self.action in ['create', 'update', ]:
            self.permission_classes = [AllowAny, ]
        return super().get_permissions()