# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ServerView',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Address', models.CharField(max_length=50)),
                ('Name', models.CharField(max_length=50)),
                ('Date', models.DateTimeField()),
                ('Disk', models.CharField(max_length=50)),
                ('DiskUse', models.TextField()),
                ('Mem', models.CharField(max_length=50)),
                ('MemUse', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
