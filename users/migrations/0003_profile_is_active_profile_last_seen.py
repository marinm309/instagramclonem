# Generated by Django 4.0 on 2022-05-08 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_active',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_seen',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]