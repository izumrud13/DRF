import os

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, serializers
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated


from training.permissions import IsOwner, IsModerator
from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer
from users.servises import create_stripe_session, create_stripe_price

STRIPE_API = os.getenv('STRIPE_API_KEY')


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDetailAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class PaymentListAPIView(generics.ListAPIView):
    """READ ALL Payments, Добавлена фильтрация"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['paid_date']
    permission_classes = [IsAuthenticated]


class PaymentCreateApiView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        course = serializer.validated_data.get('course')
        if not course:
            raise serializers.ValidationError('Укажите курс')

        payment = serializer.save()
        stripe_price_id = create_stripe_price(payment)
        payment.payment_link, payment.payment_id = create_stripe_session(stripe_price_id)
        payment.save()
