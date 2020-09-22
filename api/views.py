from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from .models import Review, Title
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
)
from rest_framework.pagination import PageNumberPagination
from django.db.models import Avg


class CommentViewSet(CreateListDestroyViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Title, id=self.kwargs.get('id'))
        return review.comments.all()


class ReviewViewSet(CreateListDestroyViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        Title.objects.aggregate(Avg('scope'))
        serializer.save(created_by=self.request.user)
