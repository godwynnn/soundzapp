# Generated by Django 3.2 on 2021-10-23 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0010_customer_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='password',
        ),
    ]
