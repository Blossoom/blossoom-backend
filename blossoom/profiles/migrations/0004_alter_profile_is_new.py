# Generated by Django 4.0.1 on 2022-01-26 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_profile_is_new'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='is_new',
            field=models.BooleanField(default=True),
        ),
    ]