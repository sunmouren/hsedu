# Generated by Django 2.1.3 on 2019-05-07 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0020_classwork_workitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='img_url',
        ),
    ]
