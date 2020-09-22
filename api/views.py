from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from .utils import generate_confirmation_code, send_mail_to_user
from .models import User


CONFIRMATION_CODE_LEN = 10


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        confirmation_code = generate_confirmation_code(CONFIRMATION_CODE_LEN)
        data = {'email': email, 'confirmation_code': confirmation_code}
        serializer = UserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        send_mail_to_user(email, confirmation_code)
        return Response({'confirmation_code': confirmation_code})


class TokenView(APIView):
    permission_classes = (AllowAny, )

    def get_token(self, user):
        token = '' # не разобрался пока как вытаскивать токен
        return token

    def post(self, request):
        user = get_object_or_404(User, email=request.data.get('email'))
        if user.confirmation_code != request.data.get('confirmation_code'):
            response = {'confirmation_code': 'Неверный код для данного email'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        response = {'token': self.get_token(user)}
        return Response(response, status=status.HTTP_200_OK)
