from django.urls import path
from .views import RegisterView, TokenView

urlpatterns = [
    path('v1/auth/email/', RegisterView.as_view(),
         name='get_confirmation_code'),
    path('v1/auth/token/', TokenView.as_view(), name='get_token'),
]
