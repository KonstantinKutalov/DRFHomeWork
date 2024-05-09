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
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(operation_summary="Получение списка пользователей")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Создание пользователя")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Получение информации о пользователе")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Обновление информации о пользователе",
                         request_body=UserSerializer)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Частичное обновление информации о пользователе",
                         request_body=UserSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Удаление пользователя")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [filters.OrderingFilter, django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']

    @swagger_auto_schema(operation_summary="Получение списка платежей")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Создание платежа")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Получение информации о платеже")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Обновление информации о платеже",
                         request_body=PaymentSerializer)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Частичное обновление информации о платеже",
                         request_body=PaymentSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Удаление платежа")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# Регистрация
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    @swagger_auto_schema(operation_summary="Регистрация нового пользователя")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# Оплата

class PaymentView(APIView):

    @swagger_auto_schema(
        operation_summary="Создание платежа",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'course_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID курса"),
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description="Сумма платежа"),
            },
            required=['course_id', 'amount'],
        ),
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'checkout_url': openapi.Schema(type=openapi.TYPE_STRING, description="URL для оплаты"),
            },
        )}
    )
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
        success_url = 'http://127.0.0.1:8000/success'
        cancel_url = 'http://127.0.0.1:8000/cancel'
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
