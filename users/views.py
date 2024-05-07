import django_filters
from rest_framework import viewsets, filters, permissions, generics
from .models import Payment
from .serializers import PaymentSerializer
from .models import User
from .serializers import UserSerializer
from .filters import PaymentFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from courses.models import Course
from decimal import Decimal, InvalidOperation
from .stripe_service import create_stripe_product, create_stripe_price, create_stripe_checkout_session


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']


# Регистрация
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer


# Оплата

class PaymentView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        amount = request.data.get('amount')

        # Проверка наличия данных
        if not course_id or not amount:
            return Response({'error': 'course_id and amount are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Получение курса
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

        # Валидация суммы (необязательно)
        try:
            amount = Decimal(amount)
        except InvalidOperation:
            return Response({'error': 'Invalid amount format'}, status=status.HTTP_400_BAD_REQUEST)

        # Создание продукта и цены в Stripe
        stripe_product = create_stripe_product(course.title, course.description)
        stripe_price = create_stripe_price(stripe_product.id, int(amount * 100))  # Сумма в копейках

        # Создание сессии оплаты
        success_url = 'https://yourdomain.com/success'
        cancel_url = 'https://yourdomain.com/cancel'
        stripe_session = create_stripe_checkout_session(stripe_price.id, success_url, cancel_url)

        # Сохранение платежа
        payment = Payment.objects.create(
            user=user,
            course=course,
            amount=amount,
            stripe_session_id=stripe_session.id,
        )

        # Возврат ссылки на оплату
        return Response({'checkout_url': stripe_session.url}, status=status.HTTP_200_OK)
