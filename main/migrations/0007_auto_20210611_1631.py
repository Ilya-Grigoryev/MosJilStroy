# Generated by Django 3.2 on 2021-06-11 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_document_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='project',
            name='start_date',
        ),
    ]