# Generated by Django 2.1.3 on 2019-01-06 13:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter_number', models.PositiveIntegerField(default=1)),
                ('title', models.CharField(max_length=64)),
                ('overview', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '章节',
                'verbose_name_plural': '章节',
                'ordering': ('chapter_number',),
            },
        ),
        migrations.CreateModel(
            name='ClassGrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('students_count', models.PositiveIntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '班级',
                'verbose_name_plural': '班级',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('overview', models.TextField()),
                ('image', models.ImageField(default='image/bg_course.jpg', upload_to='image/course')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '课程',
                'verbose_name_plural': '课程',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('overview', models.TextField(blank=True, null=True)),
                ('url', models.CharField(max_length=256)),
                ('minute', models.PositiveIntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Chapter')),
            ],
            options={
                'verbose_name': '视频',
                'verbose_name_plural': '视频',
                'ordering': ('created',),
            },
        ),
        migrations.AddField(
            model_name='classgrade',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course'),
        ),
        migrations.AddField(
            model_name='classgrade',
            name='students',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chapter',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course'),
        ),
    ]
