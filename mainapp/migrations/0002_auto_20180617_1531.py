# Generated by Django 2.0.5 on 2018-06-17 10:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='действительная'),
        ),
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='действительный'),
        ),
    ]
