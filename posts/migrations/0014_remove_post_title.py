# Generated by Django 4.0 on 2022-07-23 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_alter_post_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='title',
        ),
    ]
