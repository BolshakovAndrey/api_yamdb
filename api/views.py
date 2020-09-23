from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from .models import Review
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
)
from rest_framework.pagination import PageNumberPagination


class CommentViewSet(CreateListDestroyViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('id'))
        return review.comments.all()


class ReviewViewSet(CreateListDestroyViewSet):
    queryset = get_object_or_404(Review, id=self.kwargs.get('id'))
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly)
    pagination_class = PageNumberPagination
