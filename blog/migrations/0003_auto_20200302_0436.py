# Generated by Django 3.0.2 on 2020-03-01 23:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='content',
            new_name='reply',
        ),
    ]
