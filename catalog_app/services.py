from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail

from catalog_app.models import Category


def send_register_mail(record, email):
    send_mail(
        "Поздравляем! Ваша статья достигла 100 просмотров.",
        f"Ваша статья '{record.title}' достигла 100 просмотров. Продолжайте в том же духе!",
        settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )


def get_cache_categories():
    queryset = Category.objects.all()
    if settings.CACHE_ENABLED:
        key = 'categories'
        cache_data = cache.get(key)
        if cache_data is None:
            cache_data = queryset
            cache.set(key, cache_data)
        return cache_data
    return queryset
