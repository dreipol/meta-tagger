# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
        ('filer', '0002_auto_20150606_2003'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetaTagPageExtension',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('robots_indexing', models.BooleanField(default=True, verbose_name='Allow Indexing')),
                ('robots_following', models.BooleanField(default=True, verbose_name='Allow Following')),
                ('extended_object', models.OneToOneField(editable=False, to='cms.Page', on_delete=django.db.models.deletion.CASCADE)),
                ('og_image', filer.fields.image.FilerImageField(null=True, to='filer.Image', blank=True, verbose_name='Open Graph image', on_delete=django.db.models.deletion.CASCADE)),
                ('public_extension', models.OneToOneField(editable=False, null=True, to='meta_tagger.MetaTagPageExtension', related_name='draft_extension', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'verbose_name': 'Meta Tag',
            },
        ),
    ]
