from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import PostViewSet, FollowViewSet, CommentViewSet, GroupViewSet

router = DefaultRouter()
router.register('groups', GroupViewSet, basename='groups')
router.register('posts', PostViewSet)
router.register(r'follow', FollowViewSet, basename='followers')
router.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments'
)
urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
