from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import FollowViewSet, PostViewSet, GroupViewSet, CommentViewSet

router = DefaultRouter()
router.register('follow', FollowViewSet, basename='follow')
router.register('posts', PostViewSet, basename='posts')
router.register('groups', GroupViewSet, basename='groups')
# router.register(
#     r'posts/(?P<post_id>\d+)/comments$',
#     CommentViewSet, basename='comments'
# )

urlpatterns = [
    path('v1/posts/<int:post_id>/comments/',
         CommentViewSet.as_view({'get': 'list'}), name='comments'),
    path('v1/posts/<int:post_id>/comments/<int:comment_id>/',
         CommentViewSet.as_view({'get': 'retrieve'}),
         name='comment-detail'),

    path('v1/', include(router.urls)),
]
urlpatterns += router.urls
