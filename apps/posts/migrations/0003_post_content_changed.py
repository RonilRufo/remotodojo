# Generated by Django 3.2.10 on 2021-12-19 10:12

import django.utils.timezone
import model_utils.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_post_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content_changed',
            field=model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='content'),
        ),
    ]