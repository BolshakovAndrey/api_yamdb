from django.db.models import Avg, Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import (ListAPIView, UpdateAPIView,
                                     get_object_or_404)
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

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
    По полученному email создает user в базе, генерирует код, отправляет
    код на email. Если email уже был в базе - отправляет уже существующий
    код повторно.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email)
        if len(user) > 0:  # проверка на случай если такой email уже создан в БД
            confirmation_code = user[0].confirmation_code
        else:
            confirmation_code = generate_confirmation_code()
            max_id = User.objects.aggregate(Max('id'))['id__max'] + 1  # username обязательное поле,
            # поэтому чтобы генерировать уникальный username - беру max_id из БД
            # и генерю username=User+уникальный id
            data = {'email': email, 'confirmation_code': confirmation_code,
                    'username': f'{BASE_USERNAME}{max_id}'}
            serializer = UserSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        send_mail_to_user(email, confirmation_code)
        return Response({'email': email})


class TokenView(APIView):
    """
    По полученным email+confirmation_code генерирует и возвращает токен
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
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = (IsAuthenticated, IsSuperuser | IsAdmin,)


class UsersMeViewSet(ListAPIView, UpdateAPIView, GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):  # для PUT/PATCH по умолчанию нужен адрес вида /users/<pk>/
        # но т.к. нам нужен адрес users/me/ - переопределяю get_object чтобы просто user-а текущего возвращал
        return self.request.user

    def get_queryset(self):
        return self.get_object()

    def list(self, request, *args, **kwargs):  # по умолчанию list возвращает list, а нужен один объект
        # поэтому переопреляю list (RetriveAPIView не подходит, т.к. ему тоже нужен адрес вида /users/<pk>/)
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=False)
        return Response(serializer.data)


class TitlesViewSet(ModelViewSet):
    """
    Viewset который предоставляет CRUD-действия для произведений
    """
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).order_by('id')
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
