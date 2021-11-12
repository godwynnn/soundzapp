# Generated by Django 3.2 on 1980-01-01 01:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Beat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.IntegerField(blank=True, default=0, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='beat/image')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('genre', models.CharField(blank=True, choices=[('Afro', 'Afro'), ('Afro-pop', 'Afro-pop'), ('Pop', 'Pop'), ('Hip-pop', 'Hip-pop')], max_length=100, null=True)),
                ('sample', models.FileField(blank=True, null=True, upload_to='beat/sample_audio')),
                ('full_beat', models.FileField(blank=True, null=True, upload_to='beat/full_audio')),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('second_name', models.CharField(blank=True, max_length=100, null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_joined'],
            },
        ),
        migrations.CreateModel(
            name='OrderBeat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_ordered', models.BooleanField(default=False)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('beat', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='frontend.beat')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='frontend.customer')),
            ],
            options={
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('ordered_date', models.DateTimeField()),
                ('beats', models.ManyToManyField(to='frontend.OrderBeat')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='frontend.customer')),
            ],
            options={
                'ordering': ['-ordered_date'],
            },
        ),
    ]