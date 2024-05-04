from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import validate_link


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        extra_kwargs = {
            'video_link': {'validators': [validate_link]},
        }


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_lesson_count(self, obj):
        """
        Функция для подсчета количества уроков в курсе.
        """
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=obj).exists()


