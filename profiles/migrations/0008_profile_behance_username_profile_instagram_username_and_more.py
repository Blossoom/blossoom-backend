# Generated by Django 4.0.1 on 2022-02-01 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_profile_background_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='behance_username',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='instagram_username',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='twitter_username',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='website_url',
            field=models.URLField(blank=True, max_length=100),
        ),
    ]
