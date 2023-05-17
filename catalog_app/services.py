from django.conf import settings
from django.core.mail import send_mail


def send_register_mail(record, email):
    send_mail(
        "Поздравляем! Ваша статья достигла 100 просмотров.",
        f"Ваша статья '{record.title}' достигла 100 просмотров. Продолжайте в том же духе!",
        settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )
