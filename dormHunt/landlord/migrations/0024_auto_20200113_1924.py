# Generated by Django 3.0.1 on 2020-01-13 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landlord', '0023_addtenant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addtenant',
            name='account_user',
            field=models.EmailField(max_length=60),
        ),
    ]