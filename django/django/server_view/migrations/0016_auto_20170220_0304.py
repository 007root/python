# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server_view', '0015_serverview_redisuse'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serverview',
            name='id',
        ),
        migrations.AlterField(
            model_name='serverview',
            name='Address',
            field=models.CharField(max_length=50, serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
