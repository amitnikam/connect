# Generated by Django 3.0.2 on 2020-02-25 04:23

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
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(default='default.png', upload_to='profile_pics')),
                ('bio', models.TextField(blank=True, null=True)),
                ('profession', models.CharField(blank=True, max_length=30, null=True)),
                ('full_name', models.CharField(blank=True, max_length=30, null=True)),
                ('contact_me_at', models.TextField(blank=True, null=True)),
                ('skill_1', models.CharField(blank=True, max_length=30, null=True)),
                ('skill_2', models.CharField(blank=True, max_length=30, null=True)),
                ('skill_3', models.CharField(blank=True, max_length=30, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]