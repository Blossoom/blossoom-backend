# Generated by Django 4.0.1 on 2022-01-29 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='description',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
