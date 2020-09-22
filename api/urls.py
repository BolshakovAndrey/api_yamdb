from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, TokenView, UsersViewSet, UsersMeViewSet

router = DefaultRouter()
router.register(r'users/me', UsersMeViewSet, basename='users_me')
router.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/email/', RegisterView.as_view(),
         name='get_confirmation_code'),
    path('v1/auth/token/', TokenView.as_view(), name='get_token'),
]
