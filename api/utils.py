import random
import string

from django.core.mail import send_mail

CONFIRMATION_CODE_LEN = 10


def send_mail_to_user(email, confirmation_code):
    send_mail(
        subject='Регистрация на Yamdb, код подтверждения',
        message='Спасибо за регистрацию в нашем сервисе. '
                f'Код подтверждения: {confirmation_code}',
        from_email='register@yambd.fake',
        recipient_list=[email],
        fail_silently=False,
    )


def generate_confirmation_code():
    return ''.join(random.choices(string.digits + string.ascii_uppercase,
                                  k=CONFIRMATION_CODE_LEN))
