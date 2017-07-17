# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server_view', '0017_delete_serverview'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServerView',
            fields=[
                ('Address', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('Name', models.CharField(max_length=50)),
                ('Date', models.DateField()),
                ('Disk', models.CharField(max_length=50)),
                ('DiskUse', models.TextField()),
                ('Mem', models.CharField(max_length=50)),
                ('MemUse', models.TextField()),
                ('RedisUse', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
