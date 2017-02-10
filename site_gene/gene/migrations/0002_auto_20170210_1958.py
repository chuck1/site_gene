# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gene', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='father',
            field=models.ForeignKey(related_name='person_father', blank=True, to='gene.Person', null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='mother',
            field=models.ForeignKey(related_name='person_mother', blank=True, to='gene.Person', null=True),
        ),
    ]
