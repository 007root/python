# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server_view', '0010_serverviews'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ServerViews',
            new_name='ServerView',
        ),
    ]
