# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-06 18:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nest_graph', '0004_auto_20160206_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicestate',
            name='device',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='nest_graph.Device'),
            preserve_default=False,
        ),
    ]
