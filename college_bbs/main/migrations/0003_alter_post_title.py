# Generated by Django 3.2.9 on 2022-03-14 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_post_agree_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=255, null=True, verbose_name='问题标题'),
        ),
    ]
