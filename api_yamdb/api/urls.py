from django.urls import include, path
# from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter   #  , DefaultRouter

from .views import (CategoryViewSet, GenreViewSet, SignUpView,
                    TitleViewSet, TokenView, UsersViewSet)

router = SimpleRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('users', UsersViewSet, basename='users')
# router.register(r'posts/(?P<post_id>\d+)/comments',
#                CommentViewSet, basename='comment')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', TokenView.as_view(), name='token'),
]


# router = routers.DefaultRouter()
# router.register('users', views.UsersViewSet, basename='users')
