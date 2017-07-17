# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server_view', '0011_auto_20170220_0151'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ServerView',
        ),
    ]
