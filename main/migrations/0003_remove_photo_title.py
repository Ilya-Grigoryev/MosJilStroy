# Generated by Django 3.2 on 2021-04-17 22:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210417_1211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='title',
        ),
    ]
