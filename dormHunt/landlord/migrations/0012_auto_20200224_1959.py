# Generated by Django 3.0.1 on 2020-02-24 11:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landlord', '0011_auto_20200224_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenses',
            name='expense_balance',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='expenses',
            name='expense_date_paid',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='expenses',
            name='expense_is_paid',
            field=models.BooleanField(default=True),
        ),
    ]
