# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import TREC.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=60)),
                ('task_url', models.URLField(blank=True)),
                ('description', models.CharField(max_length=256)),
                ('year', models.IntegerField()),
                ('judgement_file', models.FileField(upload_to=b'judgements/')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=64)),
                ('track_url', models.URLField(blank=True)),
                ('description', models.CharField(max_length=256)),
                ('genre', models.CharField(max_length=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75)),
                ('profilePic', models.ImageField(upload_to=TREC.models.user_profilepic_directory_path)),
                ('website', models.URLField(blank=True)),
                ('display_name', models.CharField(max_length=50)),
                ('organisation', models.CharField(max_length=50)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='task',
            name='track',
            field=models.ForeignKey(to='TREC.Track'),
            preserve_default=True,
        ),
    ]
