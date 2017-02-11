# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userDb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='isWorker',
            field=models.BooleanField(default=False),
        ),
    ]
