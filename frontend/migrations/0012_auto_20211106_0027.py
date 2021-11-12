# Generated by Django 3.2 on 2021-11-05 23:27

from django.db import migrations, models
import frontend.formatchecker


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0011_remove_customer_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beat',
            name='full_beat',
            field=frontend.formatchecker.ContentTypeRestrictedFileField(blank=True, null=True, upload_to='beat/full_audio'),
        ),
        migrations.AlterField(
            model_name='beat',
            name='image',
            field=models.ImageField(blank=True, default='beat/image/stickers.jpg', null=True, upload_to='beat/image'),
        ),
        migrations.AlterField(
            model_name='beat',
            name='sample',
            field=frontend.formatchecker.ContentTypeRestrictedFileField(blank=True, null=True, upload_to='beat/sample_audio'),
        ),
    ]
