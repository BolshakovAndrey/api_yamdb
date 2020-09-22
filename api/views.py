from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly

from api.filters import TitleFilter
from api.models import Category, Genre, Title
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer)


class TitlesViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the CRUD actions with titles
    """
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination


class CreateListDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """
    A viewset that provides `list`, `create` and 'destroy' actions.
    """

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CategoryViewSet(CreateListDestroyViewSet):
    """
    Returns a list, creates new, and deletes existing categories
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminUser, IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    lookup_field = 'slug'



class GenreViewSet(CreateListDestroyViewSet):
    """
    Returns a list, creates new, and deletes existing genre
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminUser, IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    lookup_field = 'slug'
