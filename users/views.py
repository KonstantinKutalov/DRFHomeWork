from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer
from .models import User
from .serializers import UserSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
