# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Forum81Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_episode', models.IntegerField()),
                ('last_episode', models.IntegerField()),
                ('author', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('datePosted', models.DateTimeField()),
                ('url', models.URLField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ThreadItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('title', models.CharField(max_length=200)),
                ('episode', models.IntegerField()),
                ('torrent', models.CharField(max_length=1000)),
                ('forumItem', models.ForeignKey(to='tvb.Forum81Item')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
