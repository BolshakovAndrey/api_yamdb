from api.filters import TitleFilter
from django.db.models import Max, Avg
from rest_framework import status
from rest_framework.generics import (
    get_object_or_404, ListAPIView, UpdateAPIView)
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin, DestroyModelMixin)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from .serializers import (
    UserSerializer, CommentSerializer, ReviewSerializer,
    CategorySerializer, GenreSerializer, TitleCreateSerializer,
    TitleListSerializer)
from .utils import generate_confirmation_code, send_mail_to_user
from .models import User, Review, Category, Genre, Title
from .permissions import (
    IsAdminOrReadOnly, IsSuperuser, IsAdmin, IsAuthor, IsModerator)
from django_filters.rest_framework import DjangoFilterBackend


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
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        send_mail_to_user(email, confirmation_code)
        return Response({'email': email})


class TokenView(APIView):
    """
    Вью, принимает email и confirmation_code, возвращает токен
    """
    permission_classes = (AllowAny, )

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


class UsersMeViewSet(ListAPIView, UpdateAPIView, GenericViewSet):
    """
    Вьюсет, возвращает текущего пользователя (себя) и позволяет его изменять
    """
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return self.get_object()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=False)
        return Response(serializer.data)


class TitlesViewSet(ModelViewSet):
    """
    Viewset который предоставляет CRUD-действия для произведений
    """
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
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
    pass


class CategoryViewSet(CreateListDestroyViewSet):
    """
    Возвращает список, создает новые и удаляет существующие категории
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    # filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    """
    Возвращает список, создает новые и удаляет существующие жанры
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    # filter_backends = [SearchFilter, DjangoFilterBackend]
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
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
