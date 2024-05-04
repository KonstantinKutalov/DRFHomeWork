from django.core.exceptions import ValidationError
from urllib.parse import urlparse


def validate_link(value):
    """
    Проверка, является ли ссылка ссылкой на YouTube.
    """
    parsed_url = urlparse(value)
    if parsed_url.netloc not in ('www.youtube.com', 'youtube.com'):
        raise ValidationError("Ссылка должна быть на YouTube.")
