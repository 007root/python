# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server_view', '0002_auto_20170208_0103'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ServerView',
        ),
    ]
