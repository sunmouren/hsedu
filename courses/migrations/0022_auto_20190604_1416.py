# Generated by Django 2.1.3 on 2019-06-04 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0021_remove_video_img_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workitem',
            name='user',
        ),
        migrations.DeleteModel(
            name='WorkItem',
        ),
    ]
