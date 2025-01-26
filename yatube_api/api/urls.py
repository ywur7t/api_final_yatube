from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FollowViewSet, PostViewSet

# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.views import TokenRefreshView
# from rest_framework_simplejwt.views import TokenVerifyView
from api.views import CommentViewSet
# from djoser.views import TokenCreateView
from api.views import GroupViewSet


# router = DefaultRouter()
# router.register(r'follow', FollowViewSet, basename='follow')
# router.register(r'posts', PostViewSet, basename='post')
# router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
#                 basename='comments')


# router.register(r'groups', GroupViewSet, basename='group')
# router.register(r'groups/(?P<group_id>\d+)/', GroupViewSet,
#                 basename='groups')


# urlpatterns = [

#     path('api/v1/', include('djoser.urls')),
#     path('api/v1/', include('djoser.urls.jwt')),
#     path('', include(router.urls)),
#     path('api/token/', TokenObtainPairView.as_view(),
#          name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(),
#          name='token_refresh'),
#     path('v1/', include(router.urls)),
#     path('api/v1/', include(router.urls)),
#     path('api/v1/jwt/verify/', TokenVerifyView.as_view(),
# name='token_verify'),
#     path('api/v1/groups/<int:group_id>/', GroupViewSet, name='group'),

#     path('v1/', include('djoser.urls.jwt')),
#     path('api/v1/jwt/create/', TokenCreateView.as_view(), name='jwt_create'),
#     path('api/v1/jwt/refresh/', TokenRefreshView.as_view(),
# name='jwt_refresh')

# ]


router_v1 = DefaultRouter()
router_v1.register(r'posts', PostViewSet, basename='posts')
router_v1.register(r'groups', GroupViewSet, basename='groups')
router_v1.register(r'posts/(?P<post_id>\d+)/comments',
                   CommentViewSet, basename='comments')
router_v1.register(r'follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router_v1.urls)),

]
