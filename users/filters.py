import django_filters
from .models import Payment
from courses.models import Course, Lesson


class PaymentFilter(django_filters.FilterSet):
    course = django_filters.ModelChoiceFilter(queryset=Course.objects.all())
    lesson = django_filters.ModelChoiceFilter(queryset=Lesson.objects.all())
    payment_method = django_filters.ChoiceFilter(choices=Payment.PAYMENT_METHOD_CHOICES)

    class Meta:
        model = Payment
        fields = ['course', 'lesson', 'payment_method']
        ordering = ['-payment_date']

