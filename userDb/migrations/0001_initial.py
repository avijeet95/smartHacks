# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.IntegerField(default=0)),
                ('fname', models.CharField(max_length=20)),
                ('lname', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('gender', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=200)),
                ('aadhar', models.CharField(max_length=10)),
                ('credit', models.IntegerField(default=0)),
            ],
        ),
    ]
