# Generated by Django 4.2.6 on 2023-10-31 23:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calender', '0007_remove_events_start'),
    ]

    operations = [
        migrations.RenameField(
            model_name='events',
            old_name='end',
            new_name='expiration_dt',
        ),
    ]
