# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server_view', '0013_serverview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serverview',
            name='Date',
            field=models.DateField(),
            preserve_default=True,
        ),
    ]
