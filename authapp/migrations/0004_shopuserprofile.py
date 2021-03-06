# Generated by Django 2.2 on 2021-04-08 10:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0003_auto_20210404_2042'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopUserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('tags', models.CharField(blank=True, max_length=128, verbose_name='Теги')),
                ('about_me', models.TextField(blank=True, verbose_name='О себе')),
                ('gender', models.CharField(blank=True, choices=[('m', 'Мужской'), ('w', 'Женский')], max_length=1, verbose_name='Пол')),
            ],
        ),
    ]
