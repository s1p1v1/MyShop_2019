# Generated by Django 2.0.5 on 2018-06-17 10:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='действительный'),
        ),
    ]