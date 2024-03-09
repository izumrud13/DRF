from django.contrib.auth.models import AbstractUser
from django.db import models

from training.models import Course, Lesson

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """Модель таблицы User"""
    username = None

    email = models.EmailField(unique=True, verbose_name='Почта')
    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)
    city = models.CharField(max_length=25, verbose_name='Город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        """Класс отображения метаданных"""
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    """Модель таблицы Оплаты"""
    class PaymentType(models.TextChoices):
        CASH = 'cash', "наличные"
        BANK = 'bank', 'перевод'

    payer = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='плательщик', related_name='payer')
    date_of_payment = models.DateField(auto_now=True, verbose_name='Дата оплаты')
    payed_course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Оплаченный курс')
    payed_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Оплаченный урок')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Сумма оплаты')
    payment_type = models.CharField(max_length=20, choices=PaymentType.choices, verbose_name='Способ оплаты')

    def __str__(self):
        return f'{self.payer} - {self.payed_course if self.payed_course else self.payed_lesson} - {self.amount}'

    class Meta:
        verbose_name = 'оплата'
        verbose_name_plural = 'оплаты'
        ordering = ('payer', 'date_of_payment')
