# Generated by Django 2.1.3 on 2019-02-28 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_classgrade_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='play_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
