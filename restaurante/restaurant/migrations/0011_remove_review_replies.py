# Generated by Django 3.1 on 2021-01-24 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0010_auto_20210124_1139'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='replies',
        ),
    ]