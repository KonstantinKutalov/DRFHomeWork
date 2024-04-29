import django_filters
from rest_framework import viewsets, filters,permissions,generics
from .models import Payment
from .serializers import PaymentSerializer
from .models import User
from .serializers import UserSerializer
from .filters import PaymentFilter


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