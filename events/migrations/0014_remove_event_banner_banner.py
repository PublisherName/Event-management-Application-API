# Generated by Django 5.1.2 on 2024-12-02 06:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_remove_event_location_location_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='banner',
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='event_banners/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='banners', to='events.event')),
            ],
        ),
    ]