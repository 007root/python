# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server_view', '0005_auto_20170220_0125'),
    ]

    operations = [
        migrations.AddField(
            model_name='serverview',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=1, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='serverview',
            name='Address',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='serverview',
            name='Date',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
