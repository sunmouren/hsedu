# Generated by Django 2.1.3 on 2019-02-19 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_userprofile_avatar_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar_url',
            field=models.CharField(default='http://storage.haishionline.com/image/avatar/default.jpg', max_length=200),
        ),
    ]
