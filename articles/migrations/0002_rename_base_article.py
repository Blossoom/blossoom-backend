# Generated by Django 4.0.1 on 2022-01-22 17:05

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tags', '0001_initial'),
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Base',
            new_name='Article',
        ),
    ]
