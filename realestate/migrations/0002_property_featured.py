# Generated by Django 5.0.4 on 2024-05-12 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realestate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]
