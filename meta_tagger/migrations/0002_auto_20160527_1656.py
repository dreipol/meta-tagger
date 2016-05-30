# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meta_tagger', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='metatagpageextension',
            name='og_image_height',
            field=models.PositiveIntegerField(blank=True, verbose_name='Open Graph image height', null=True),
        ),
        migrations.AddField(
            model_name='metatagpageextension',
            name='og_image_width',
            field=models.PositiveIntegerField(blank=True, verbose_name='Open Graph image width', null=True),
        ),
    ]
