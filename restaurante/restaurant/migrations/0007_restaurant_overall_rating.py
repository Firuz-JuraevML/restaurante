# Generated by Django 3.1 on 2021-01-24 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0006_auto_20210122_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='overall_rating',
            field=models.FloatField(default=0.0),
        ),
    ]