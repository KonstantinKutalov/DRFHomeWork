from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from users.tasks import deactivate_inactive_users
    # Задача деактивации неактивных пользователей
    sender.add_periodic_task(
        crontab(day_of_month='1'),  # Запускается 1-го числа каждого месяца
        deactivate_inactive_users.s(),
        name='deactivate_inactive_users'
    )
