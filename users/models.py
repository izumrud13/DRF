from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone

from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from training.models import Course, Lesson

NULLABLE = {'blank': True, 'null': True}


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Поле Email должно быть заполнено')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    """Модель таблицы User"""
    username = None

    email = models.EmailField(unique=True, verbose_name='Почта')
    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)
    city = models.CharField(max_length=25, verbose_name='Город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        """Класс отображения метаданных"""
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    class PaymentType(models.TextChoices):
        CASH = "CASH", "Наличные"
        TRANSFER_TO_ACCOUNT = 'TRANSFER_TO_ACCOUNT', 'Перевод на счет'

    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='payments',
                             null=True, blank=True)
    paid_date = models.DateTimeField(default=timezone.now, verbose_name='Дата оплаты')
    course = models.ForeignKey('training.Course', on_delete=models.CASCADE, verbose_name='Оплаченный курс', null=True,
                               blank=True)
    lesson = models.ForeignKey('training.Lesson', on_delete=models.CASCADE, verbose_name='Оплаченный урок', null=True,
                               blank=True)
    amount = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=50, choices=PaymentType.choices, default='TRANSFER_TO_ACCOUNT',
                                      verbose_name='Способ оплаты')
    payment_link = models.URLField(max_length=400, verbose_name='Ссылка на оплату', null=True, blank=True)
    payment_id = models.CharField(max_length=255, verbose_name='Идентификатор платежа', unique=True, null=True,
                                  blank=True)

    def __str__(self):
        return f'{self.user} - {self.paid_date} - {self.payment_method}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
