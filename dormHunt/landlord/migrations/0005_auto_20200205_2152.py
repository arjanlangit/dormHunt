# Generated by Django 3.0.1 on 2020-02-05 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landlord', '0004_auto_20200123_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='slots',
            field=models.IntegerField(default=0),
        ),
    ]
