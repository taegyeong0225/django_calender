# Generated by Django 4.2.6 on 2023-10-31 22:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calender', '0003_remove_events_end_remove_events_start_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='events',
            old_name='end_date',
            new_name='expiration_dt',
        ),
    ]
