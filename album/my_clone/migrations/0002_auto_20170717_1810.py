# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-17 18:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_clone', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='creation_date',
            field=models.DateTimeField(default='17.07.2017'),
        ),
    ]