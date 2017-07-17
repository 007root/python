# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server_view', '0014_auto_20170220_0203'),
    ]

    operations = [
        migrations.AddField(
            model_name='serverview',
            name='RedisUse',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
