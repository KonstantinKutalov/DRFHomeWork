from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255)
    preview = models.ImageField(upload_to='course_previews/', blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['title']

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    preview = models.ImageField(upload_to='lesson_previews/', blank=True)
    video_link = models.URLField(blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['course', 'title']

    def __str__(self):
        return f"{self.title} ({self.course.title})"
