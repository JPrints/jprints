# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-12 11:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import publications.models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0003_auto_20160812_1213'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_type', models.CharField(choices=[('dra', 'draft'), ('sub', 'submitted'), ('acc', 'accepted'), ('pub', 'published'), ('upd', 'updated'), ('sup', 'supplemental'), ('cov', 'coverimage'), ('dat', 'dataset'), ('pre', 'presentation'), ('oth', 'other')], default='dra', max_length=3)),
                ('visibility_status', models.CharField(choices=[('P', 'Public'), ('R', 'Restricted'), ('E', 'Embagoed'), ('N', 'None')], default='N', max_length=1)),
                ('licence', models.CharField(blank=True, choices=[('publi', 'publisher'), ('cc_by', 'cc_by'), ('by_nc', 'cc_by_nc'), ('by_nd', 'cc_by_nd'), ('nc_nd', 'cc_by_nc_nd'), ('nc_sa', 'cc_by_nc_sa'), ('by_sa', 'cc_by_sa'), ('cc_pd', 'cc_public_domain')], max_length=5)),
                ('embargo', models.DateField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('filefield', models.FileField(blank=True, upload_to=publications.models.Document.pub_doc_path)),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publications.Publication')),
            ],
        ),
    ]
