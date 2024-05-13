from config.celery import app
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


@app.task
def send_course_update_email(user_email, course_title):
    """
    Отправляет email пользователю об обновлении курса.

    Args:
        user_email (str): Email пользователя.
        course_title (str): Название обновленного курса.
    """
    subject = f'Обновление курса "{course_title}"'
    message = render_to_string('courses/course_update_email.html', {'course_title': course_title})
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list, html_message=message)

