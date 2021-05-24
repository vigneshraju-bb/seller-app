# Generated by Django 3.2.3 on 2021-05-20 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('seller_id', models.AutoField(primary_key=True, serialize=False)),
                ('seller_name', models.CharField(max_length=250)),
                ('seller_address', models.TextField(null=True)),
                ('seller_mobile', models.CharField(max_length=100)),
                ('seller_otp', models.CharField(max_length=50)),
                ('seller_status', models.SmallIntegerField()),
                ('seller_created_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'tbl_seller',
                'ordering': ['seller_name'],
            },
        ),
    ]