from django.conf import settings
from django.db import models

# Create your models here.
NULLABLE = {'blank': True, 'null': True}


class Subscription(models.Model):
    """Модедь подписки"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='subscription')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='Курс', related_name='subscription')

    def __str__(self):
        return f'{self.user} - {self.course}'

    class Meta:
        """Класс отображения метаданных"""
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Course(models.Model):
    """Модель таблицы Курсы"""
    name = models.CharField(max_length=100, verbose_name='Название')
    preview = models.ImageField(upload_to='previews/', null=True, blank=True, verbose_name='Превью')
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              verbose_name='Автор курса', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        """Класс отображения метаданных"""
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    """Модель таблицы Уроки"""
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    preview = models.ImageField(upload_to='previews/', **NULLABLE, verbose_name='Превью')
    video_link = models.URLField(max_length=200, **NULLABLE, verbose_name='Ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Курс',
                               related_name='lesson')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор урока', null=True,
                              blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Стоимость')
    date_modified = models.DateTimeField(auto_now=True, **NULLABLE, verbose_name='Дата изменения')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        """Класс отображения метаданных"""
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
