# Generated by Django 2.2 on 2021-02-01 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_product'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name'], 'verbose_name': 'продукт', 'verbose_name_plural': 'продукты'},
        ),
        migrations.AlterModelOptions(
            name='productcategory',
            options={'ordering': ['name'], 'verbose_name': 'категория продукта', 'verbose_name_plural': 'категории продукта'},
        ),
    ]
