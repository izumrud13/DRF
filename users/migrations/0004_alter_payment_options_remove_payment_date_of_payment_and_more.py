# Generated by Django 5.0.2 on 2024-03-28 16:53

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0006_alter_lesson_date_modified'),
        ('users', '0003_alter_payment_amount_alter_payment_date_of_payment_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': 'платеж', 'verbose_name_plural': 'платежи'},
        ),
        migrations.RemoveField(
            model_name='payment',
            name='date_of_payment',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payed_course',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payed_lesson',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payer',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payment_type',
        ),
        migrations.AddField(
            model_name='payment',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='training.course', verbose_name='Оплаченный курс'),
        ),
        migrations.AddField(
            model_name='payment',
            name='lesson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='training.lesson', verbose_name='Оплаченный урок'),
        ),
        migrations.AddField(
            model_name='payment',
            name='paid_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата оплаты'),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_id',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Идентификатор платежа'),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_link',
            field=models.URLField(blank=True, max_length=400, null=True, verbose_name='Ссылка на оплату'),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('CASH', 'Наличные'), ('TRANSFER_TO_ACCOUNT', 'Перевод на счет')], default='TRANSFER_TO_ACCOUNT', max_length=50, verbose_name='Способ оплаты'),
        ),
        migrations.AddField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.PositiveIntegerField(verbose_name='Сумма оплаты'),
        ),
    ]