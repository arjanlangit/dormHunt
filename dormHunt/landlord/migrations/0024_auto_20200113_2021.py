# Generated by Django 3.0.1 on 2020-01-13 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('landlord', '0023_auto_20200113_1832'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='barangay',
        ),
        migrations.RemoveField(
            model_name='property',
            name='city',
        ),
        migrations.RemoveField(
            model_name='property',
            name='house_number',
        ),
        migrations.RemoveField(
            model_name='property',
            name='street',
        ),
        migrations.RemoveField(
            model_name='property',
            name='zip_code',
        ),
    ]
