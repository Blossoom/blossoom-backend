# Generated by Django 4.0.1 on 2022-01-25 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_rename_author_artwork_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='artwork',
            name='total_votes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='total_votes',
            field=models.IntegerField(default=0),
        ),
    ]
