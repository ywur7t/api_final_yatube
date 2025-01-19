from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import FollowViewSet, PostViewSet

router = DefaultRouter()
router.register('follow', FollowViewSet, basename='follow')
router.register('posts', PostViewSet, basename='posts')

urlpatterns = [
    path('v1/', include(router.urls)),
]
urlpatterns += router.urls
