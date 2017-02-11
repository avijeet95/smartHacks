# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userDb', '0002_person_isworker'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amt', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tid', models.IntegerField(default=0)),
                ('lon1', models.CharField(max_length=50, null=True)),
                ('lat1', models.CharField(max_length=50, null=True)),
                ('lon2', models.CharField(max_length=50, null=True)),
                ('lat2', models.CharField(max_length=50, null=True)),
                ('budget', models.IntegerField(default=0)),
                ('weight', models.IntegerField(default=1)),
                ('desc', models.CharField(max_length=200)),
                ('uid', models.ForeignKey(to='userDb.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.CharField(max_length=50, null=True)),
                ('destination', models.CharField(max_length=50, null=True)),
                ('uid', models.ForeignKey(to='userDb.Person')),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='tid',
            field=models.ForeignKey(to='trip.Trip'),
        ),
        migrations.AddField(
            model_name='job',
            name='uid',
            field=models.ForeignKey(related_name='userId', to='userDb.Person'),
        ),
        migrations.AddField(
            model_name='job',
            name='wid',
            field=models.ForeignKey(related_name='workId', to='userDb.Person'),
        ),
    ]
