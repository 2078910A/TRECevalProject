# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import TREC.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('TREC', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Run',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=4)),
                ('run_type', models.CharField(max_length=2, choices=[(b'MA', b'Manual'), (b'AU', b'Automatic')])),
                ('feedback_type', models.CharField(max_length=2, choices=[(b'NO', b'None'), (b'PS', b'Pseudo'), (b'RE', b'Relevance'), (b'OT', b'Other')])),
                ('query_type', models.CharField(max_length=2, choices=[(b'TI', b'Title'), (b'TD', b'Title & Description'), (b'DE', b'Description'), (b'AL', b'All'), (b'OT', b'Other')])),
                ('researcher', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(to='TREC.Task')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='task',
            name='title',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
        migrations.AlterField(
            model_name='task',
            name='judgement_file',
            field=models.FileField(upload_to=TREC.models.task_judgement_file_path),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_url',
            field=models.URLField(unique=True),
        ),
        migrations.AlterField(
            model_name='track',
            name='description',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='track',
            name='genre',
            field=models.CharField(max_length=20, choices=[(b'NE', b'News'), (b'WE', b'Web'), (b'ME', b'Medical'), (b'BL', b'Blog'), (b'LE', b'Legal')]),
        ),
        migrations.AlterField(
            model_name='track',
            name='title',
            field=models.CharField(unique=True, max_length=50),
        ),
    ]
