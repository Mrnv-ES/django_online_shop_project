# Generated by Django 2.2 on 2021-02-15 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20210201_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='активность'),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='активность'),
        ),
    ]
