# Generated by Django 3.2.9 on 2021-11-24 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20211124_1114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='create_user_id',
        ),
    ]
