from django.db.models import Avg, Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

from api.filters import TitleFilter
from .models import Category, Genre, Review, Title, User
from .permissions import (IsAdmin, IsAdminOrReadOnly, IsAuthor, IsModerator,
                          IsSuperuser)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleListSerializer,
                          UserSerializer)
from .utils import generate_confirmation_code, send_mail_to_user

BASE_USERNAME = 'User'


class RegisterView(APIView):
    """
    Вью, принимает на вход email и генерирует для него код доступа
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email)
        if len(user) > 0:
            confirmation_code = user[0].confirmation_code
        else:
            confirmation_code = generate_confirmation_code()
            max_id = User.objects.aggregate(Max('id'))['id__max'] + 1
            data = {'email': email, 'confirmation_code': confirmation_code,
                    'username': f'{BASE_USERNAME}{max_id}'}
            serializer = UserSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        send_mail_to_user(email, confirmation_code)
        return Response({'email': email})


class TokenView(APIView):
    """
    Вью, принимает email и confirmation_code, возвращает токен
    """
    permission_classes = (AllowAny,)

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def post(self, request):
        user = get_object_or_404(User, email=request.data.get('email'))
        if user.confirmation_code != request.data.get('confirmation_code'):
            response = {'confirmation_code': 'Неверный код для данного email'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        response = {'token': self.get_token(user)}
        return Response(response, status=status.HTTP_200_OK)


class UsersViewSet(ModelViewSet):
    """
    Вьюсет для работы с пользователями
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = (IsAuthenticated, IsSuperuser | IsAdmin,)

    @action(detail=False, permission_classes=(IsAuthenticated,),
            methods=['get', 'patch'], url_path='me')
    def get_or_update_self(self, request):
        if request.method != 'GET':
            serializer = self.get_serializer(
                instance=request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(request.user, many=False)
            return Response(serializer.data)


class TitlesViewSet(ModelViewSet):
    """
    Viewset который предоставляет CRUD-действия для произведений
    """
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('id')
    filter_backends = (DjangoFilterBackend, SearchFilter)
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateSerializer
        return TitleListSerializer


class CreateListDestroyViewSet(ListModelMixin,
                               CreateModelMixin,
                               DestroyModelMixin,
                               GenericViewSet):
    """
    Вьюсет, обесечивающий `list()`, `create()`, `destroy()`
    """


class CategoryViewSet(CreateListDestroyViewSet):
    """
    Возвращает список, создает новые и удаляет существующие категории
    """
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    """
    Возвращает список, создает новые и удаляет существующие жанры
    """
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name']
    lookup_field = 'slug'


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthor | IsModerator |
                          IsAdminOrReadOnly | IsSuperuser]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(
            Review.objects.filter(title_id=title_id), pk=review_id
        )
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(
            Review.objects.filter(title_id=title_id), pk=review_id
        )
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthor | IsModerator |
                          IsAdminOrReadOnly | IsSuperuser]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all().order_by('id')

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
