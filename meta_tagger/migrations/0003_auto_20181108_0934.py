# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-08 08:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('meta_tagger', '0002_auto_20160527_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='metatagpageextension',
            name='robots_disallow',
            field=models.BooleanField(default=False,
                                      help_text="Adds this page with the 'Disallow' instruction to the robots.txt file. Search engines won't crawl it. Consider deactivating the indexing checkbox above to prevent indexing too.",
                                      verbose_name='Disallow'),
        ),
        migrations.AlterField(
            model_name='metatagpageextension',
            name='robots_following',
            field=models.BooleanField(default=True, help_text='Allows search engines to follow the links on this page.',
                                      verbose_name='Allow Following'),
        ),
        migrations.AlterField(
            model_name='metatagpageextension',
            name='robots_indexing',
            field=models.BooleanField(default=True,
                                      help_text='Allows search engines to include this page in search results.',
                                      verbose_name='Allow Indexing'),
        ),
    ]
