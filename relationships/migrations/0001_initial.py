# Generated by Django 4.0.1 on 2022-01-18 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('follow_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='profiles.profile')),
                ('follow_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='profiles.profile')),
            ],
            options={
                'unique_together': {('follow_from', 'follow_to')},
            },
        ),
    ]
