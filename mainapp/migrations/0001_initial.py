# Generated by Django 2.0.5 on 2018-06-03 09:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='страна изготовления')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=128, unique=True, verbose_name='название продукта')),
                ('quality', models.TextField(blank=True, verbose_name='признаки продукта')),
                ('preference', models.TextField(blank=True, verbose_name='применение продукта')),
                ('image_src', models.ImageField(blank=True, upload_to='products_images')),
                ('producer',
                 models.CharField(blank=True, max_length=60, verbose_name='организация - изготовитель продукта')),
                ('brand', models.CharField(blank=True, max_length=60, verbose_name='фирменный знак продукта')),
                ('alco', models.CharField(blank=True, max_length=60, verbose_name='крепкость продукта')),
                ('vol', models.CharField(blank=True, max_length=5, verbose_name='объем продукта')),
                ('class_c', models.CharField(blank=True, max_length=10, verbose_name='класс продукта')),
                ('age', models.IntegerField(null=True, verbose_name='возраст продукта')),
                ('cost', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='цена продукта')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='количество на складе')),
                ('comment', models.TextField(blank=True, verbose_name='описание продукта')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Country')),
            ],
        ),
    ]
