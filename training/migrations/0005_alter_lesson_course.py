# Generated by Django 5.0.2 on 2024-03-23 06:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0004_lesson_amount_lesson_date_modified_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lesson', to='training.course', verbose_name='Курс'),
        ),
    ]