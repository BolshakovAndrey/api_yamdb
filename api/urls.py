from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import TitlesViewSet, GenreViewSet, CategoryViewSet

router_v1 = DefaultRouter()
router_v1.register(r"titles", TitlesViewSet, basename='Title')
router_v1.register(r"genres", GenreViewSet, basename='Genre')
router_v1.register(r"categories", CategoryViewSet, basename='Category')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/genres/', GenreViewSet.as_view({'get': 'list',
                                             'post': 'create',
                                             'delete': 'destroy'})),
    path('v1/category/', CategoryViewSet.as_view({'get': 'list',
                                                  'post': 'create',
                                                  'delete': 'destroy'}))
]
