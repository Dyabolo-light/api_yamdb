from django.urls import include, path
# from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter



from .views import CategoryViewSet, GenreViewSet, TitleViewSet, ReviewViewSet, CommentViewSet

router = SimpleRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='review')


router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
# router.register(r'posts/(?P<post_id>\d+)/comments',
#                CommentViewSet, basename='comment')


urlpatterns = [
    path('v1/', include(router.urls)),
]
