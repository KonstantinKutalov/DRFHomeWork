from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Course, Lesson, Subscription

User = get_user_model()


class TestCourse(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="kostian2705TEST@mail.ru", password="TESTPASWORD")
        self.admin_user = User.objects.create_superuser(email="kutalov.k.vTEST@mail.ru", password="TESTPASSWORD")
        self.course = Course.objects.create(title="Test Course", created_by=self.admin_user)
        self.lesson = Lesson.objects.create(title="Test Lesson", course=self.course, created_by=self.admin_user)

    def test_create_lesson_unauthorized(self):
        # Неавторизованный пользователь не может создать урок
        data = {'title': 'New Lesson', 'course': self.course.id}
        response = self.client.post('/api/courses/lessons/', data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_create_lesson_authorized(self):
        # Авторизованный администратор может создать урок
        self.client.force_authenticate(user=self.admin_user)
        data = {'title': 'New Lesson', 'course': self.course.id, 'created_by': self.admin_user.id}
        response = self.client.post('/api/courses/lessons/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_subscribe_unsubscribe(self):
        self.client.force_authenticate(user=self.user)

        # Подписка на курс
        response = self.client.post('/api/courses/subscribe/', {'course_id': self.course.id}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Подписка добавлена')

        # Отписка от курса
        response = self.client.post('/api/courses/subscribe/', {'course_id': self.course.id}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Подписка удалена')

    def test_list_lessons_unauthorized(self):
        # Неавторизованный пользователь не может получить список уроков
        response = self.client.get('/api/courses/lessons/')
        self.assertEqual(response.status_code, 401)

