# Generated by Django 5.0.7 on 2024-07-31 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_event_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
