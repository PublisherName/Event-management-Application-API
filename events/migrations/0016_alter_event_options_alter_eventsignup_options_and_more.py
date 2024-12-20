# Generated by Django 5.1.2 on 2024-12-02 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_schedule'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['created_at'], 'verbose_name': 'Event', 'verbose_name_plural': 'Event'},
        ),
        migrations.AlterModelOptions(
            name='eventsignup',
            options={'ordering': ['signup_date'], 'verbose_name': 'Attendee', 'verbose_name_plural': 'Attendee'},
        ),
        migrations.RemoveField(
            model_name='event',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='event',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='event',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='event',
            name='start_time',
        ),
    ]
