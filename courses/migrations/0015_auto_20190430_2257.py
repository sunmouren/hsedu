# Generated by Django 2.1.3 on 2019-04-30 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0014_auto_20190430_1940'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='view_count',
            new_name='play_count',
        ),
        migrations.AddField(
            model_name='course',
            name='view_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
