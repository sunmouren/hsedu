# Generated by Django 2.1.3 on 2019-01-13 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_auto_20190112_1948'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signin',
            name='deadline',
        ),
        migrations.AddField(
            model_name='signin',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
