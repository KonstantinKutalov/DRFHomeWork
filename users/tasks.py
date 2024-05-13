from config.celery import app
from datetime import datetime, timedelta
from django.utils import timezone
from .models import User


@app.task
def deactivate_inactive_users():
    """
    Деактивирует пользователей, которые не входили более месяца.
    """
    month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=month_ago, is_active=True)
    for user in inactive_users:
        user.is_active = False
        user.save()
