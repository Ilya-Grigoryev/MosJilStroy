# Generated by Django 3.2 on 2021-04-20 19:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_photo_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobseeker',
            name='vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.vacancy'),
            preserve_default=False,
        ),
    ]
