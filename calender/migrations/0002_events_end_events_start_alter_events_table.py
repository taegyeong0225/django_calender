# Generated by Django 4.2.5 on 2023-09-24 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calender', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='events',
            name='start',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterModelTable(
            name='events',
            table='tblevents',
        ),
    ]
