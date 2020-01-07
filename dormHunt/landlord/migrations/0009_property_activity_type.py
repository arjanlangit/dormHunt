# Generated by Django 3.0.1 on 2020-01-05 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landlord', '0008_property_tagline'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='activity_type',
            field=models.CharField(choices=[('F', 'Favorite'), ('L', 'Like'), ('U', 'Up Vote'), ('D', 'Down Vote')], max_length=1, null=True),
        ),
    ]