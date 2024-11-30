# Generated by Django 5.1.2 on 2024-11-26 08:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("preferences", "0002_remove_emailtemplate_name_emailtemplate_email_type"),
    ]

    operations = [
        migrations.RenameField(
            model_name="emailtemplate",
            old_name="body",
            new_name="body_html",
        ),
        migrations.AddField(
            model_name="emailtemplate",
            name="body_plaintext",
            field=models.TextField(default="This is a sample email template."),
            preserve_default=False,
        ),
    ]