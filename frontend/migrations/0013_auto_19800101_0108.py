# Generated by Django 3.2 on 1980-01-01 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0012_auto_20211106_0027'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='session',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='orderbeat',
            name='session',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
