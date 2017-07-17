# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server_manage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='serverlist',
            name='ServerId',
            field=models.CharField(default='s', max_length=50),
            preserve_default=False,
        ),
    ]
