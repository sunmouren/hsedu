# Generated by Django 2.1.3 on 2019-05-02 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0016_course_study_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='minute',
        ),
        migrations.AddField(
            model_name='video',
            name='duration',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
