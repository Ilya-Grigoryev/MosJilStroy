# Generated by Django 3.2 on 2021-04-17 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='title',
        ),
        migrations.AddField(
            model_name='project',
            name='construction_year',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='group',
            field=models.IntegerField(choices=[(0, 'Текущий проект'), (1, 'Сданный объект')], default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='short_description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='project',
            name='storeys',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('title', models.CharField(max_length=255)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.project')),
            ],
        ),
    ]
