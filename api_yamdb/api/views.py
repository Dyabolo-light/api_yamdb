import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Title, Review, Comment
from users.models import CustomUser
from users.utils import get_confirmation_code
from .permissions import (IsAdminOrReadOnly, IsAdministator, IsAnAuthor)
from .serializers import (CategorySerializer, GenreSerializer,
                          SignUpSerializer, Serializer,
                          TitleSerializer, TokenSerializer, UserSerializer
                         , ReviewSerializer, CommentSerializer)

from django.db.models import Avg

class ListCreateDestroyViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, IsAuthenticatedOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly, IsAuthenticatedOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name',
                                     lookup_expr='icontains')
    year = django_filters.NumberFilter(field_name='year',
                                       lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category__slug',
                                         lookup_expr='icontains')
    genre = django_filters.CharFilter(field_name='genre__slug',
                                      lookup_expr='icontains')
    class Meta:
        model = Title
        fields = '__all__'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')) #изменения которые дают рейтинг
#     queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly, IsAuthenticatedOrReadOnly)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_class = TitleFilter
    search_fields = ('name', 'year', 'genre', 'category')

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleInfoSerializer
        return TitleSerializer
      
class ReviewViewSet(viewsets.ModelViewSet):
   queryset = Review.objects.all()
   serializer_class = ReviewSerializer
#    permission_classes = (IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly)
#    pagination_class = LimitOffsetPagination

   def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        serializer.save(title_id=title_id)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        serializer.save(review_id=review_id)


class SignUpView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer

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
    serializer_class = TokenSerializer

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
    serializer_class = UserSerializer
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
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        serializer = UserSerializer(
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
