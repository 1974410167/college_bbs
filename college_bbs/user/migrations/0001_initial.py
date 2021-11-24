# Generated by Django 3.2.9 on 2021-11-24 08:28

import college_bbs.common.models.deletion
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
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('create_user_id', models.BigIntegerField(default=0, verbose_name='创建人 ID')),
                ('name', models.CharField(blank=True, help_text='姓名', max_length=100, verbose_name='姓名')),
                ('phone', models.CharField(blank=True, help_text='手机号', max_length=11, verbose_name='手机号')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='账号')),
            ],
            options={
                'db_table': 'user_userprofile',
                'abstract': False,
            },
            bases=(college_bbs.common.models.deletion.ModelOnDeleteMixin, models.Model),
        ),
    ]
