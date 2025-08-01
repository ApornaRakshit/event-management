# Generated by Django 5.2.3 on 2025-07-17 20:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_delete_project_rename_name_event_title'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='title',
            new_name='name',
        ),
        migrations.AddField(
            model_name='event',
            name='asset',
            field=models.ImageField(blank=True, default='event_asset/default_img.png', null=True, upload_to='event_asset'),
        ),
        migrations.AddField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='rsvp_events', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Participant',
        ),
    ]
