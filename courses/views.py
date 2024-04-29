import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup()

from rest_framework import viewsets, generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from users.permissions import IsOwnerOrModerator


# Для курса
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

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


# Для урока
class LessonListCreateAPIView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

    def get_permissions(self):
        if self.action == 'create':
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
