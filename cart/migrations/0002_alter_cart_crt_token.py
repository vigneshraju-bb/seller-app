# Generated by Django 3.2.3 on 2021-05-21 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='crt_token',
            field=models.TextField(default=None),
        ),
    ]
