from rest_framework.generics import GenericAPIView
from rest_framework import filters, status
from . import serializers
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from rest_framework.permissions import (AllowAny, IsAdminUser,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from .permissions import (IsUser, IsAdministator, IsModerator, IsSuperUser,
                          IsAnAuthor)
import uuid
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .utils import get_confirmation_code
from rest_framework.decorators import action


class SignUpView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.SignUpSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if CustomUser.objects.filter(username=data.get('username'),
                                     email=data.get('email')).exists():
            return Response(get_confirmation_code(data),
                            status=status.HTTP_200_OK)
        serializer.is_valid(raise_exception=True)
        if data.get('username') == 'me':
            return Response({'error': 'Restricted'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(get_confirmation_code(serializer.validated_data),
                        status=status.HTTP_200_OK)


class TokenView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.TokenSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        if not CustomUser.objects.filter(
            username=data.get('username')
        ).exists():
            return Response({'error': 'Bad request'},
                            status=status.HTTP_404_NOT_FOUND)
        if not CustomUser.objects.filter(
            confirmation_code=data.get('confirmation_code')
        ).exists():
            return Response({'error': 'Bad request'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(CustomUser, username=username)
        tokens = RefreshToken.for_user(user).access_token
        return Response({'token': str(tokens)}, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated, IsAdministator]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    http_method_names = ['get', 'patch', 'post', 'delete']
    lookup_field = 'username'
    search_fields = ('username', )

    @action(
        detail=False,
        methods=('GET', 'PATCH'),
        permission_classes=(IsAuthenticated, IsAnAuthor)
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = serializers.UserSerializer(request.user)
            return Response(serializer.data)
        serializer = serializers.UserSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data)

    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk == 'me':
            return self.request.user
        return super().get_object()

#    def get_object(self):
#        return self.request.user

#    def get_permissions(self):
#        if self.action in ['create', 'update', ]:
#            self.permission_classes = [IsAuthenticated, IsAnAuthor, ]
#        if self.action in ['list', 'update', 'destroy', 'retrieve', ]:
#            self.permission_classes = [IsAuthenticated, IsAdministator, ]
#        return super().get_permissions()
