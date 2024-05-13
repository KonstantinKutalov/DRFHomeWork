import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup()

from rest_framework import viewsets, generics
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from users.permissions import IsOwnerOrModerator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .paginators import CoursePagination, LessonPagination
from .tasks import send_course_update_email
from .models import Subscription


# Для курса
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAdminUser]  # Только администраторы могут создавать и удалять
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated,
                                  IsModerator]  # Аутентифицированные пользователи и модераторы могут обновлять
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_update(self, serializer):
        instance = serializer.save()
        # Отправка email подписчикам ообновлении курса
        subscribers = Subscription.objects.filter(course=instance).values_list('user__email', flat=True)
        for subscriber_email in subscribers:
            send_course_update_email.delay(subscriber_email, instance.title)


# Для урока
class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]
    pagination_class = LessonPagination

    def get_permissions(self):
        if self.request.method == 'POST':  # Проверка метода запроса
            permission_classes = [IsAdminUser]  # Только администраторы могут создавать
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrModerator]  # Модераторы и владельцы могут просматривать
        return [permission() for permission in permission_classes]


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [IsAdminUser]  # Только администраторы могут удалять
        else:
            permission_classes = [IsAuthenticated,
                                  IsOwnerOrModerator]  # Модераторы и владельцы могут получать и обновлять
        return [permission() for permission in permission_classes]


class SubscriptionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response({'error': 'course_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Course, pk=course_id)
        subscription, created = Subscription.objects.get_or_create(user=user, course=course)

        if created:
            message = 'Подписка добавлена'
        else:
            subscription.delete()
            message = 'Подписка удалена'

        return Response({'message': message}, status=status.HTTP_200_OK)
