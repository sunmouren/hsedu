# Generated by Django 2.1.3 on 2019-01-13 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_auto_20190113_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='signin',
            name='students_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
