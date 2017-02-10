# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('father', models.ForeignKey(related_name='person_father', to='gene.Person', null=True)),
                ('mother', models.ForeignKey(related_name='person_mother', to='gene.Person', null=True)),
            ],
        ),
    ]
