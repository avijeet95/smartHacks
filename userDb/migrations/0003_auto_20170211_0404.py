# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userDb', '0002_person_isworker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='fname',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='person',
            name='lname',
            field=models.CharField(max_length=55),
        ),
    ]
