import datetime

from django.core.mail import send_mail
from django.core.validators import MaxValueValidator

from api_yamdb.settings import FROM_EMAIL


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


def send_mail_to_user(email, confirmation_code):
    send_mail(
        subject='Регистрация на Yamdb, код подтверждения',
        message='Спасибо за регистрацию в нашем сервисе. '
                f'Код подтверждения: {confirmation_code}',
        from_email=FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
