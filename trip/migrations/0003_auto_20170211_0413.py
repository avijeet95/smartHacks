# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0002_auto_20170211_0404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='uid',
            field=models.CharField(max_length=15),
        ),
    ]
