# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-26 09:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import lily.objectfiles.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tenant', '0008_auto_20180822_1308'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjectFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=255, upload_to=lily.objectfiles.models.get_file_upload_path)),
                ('size', models.PositiveIntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('gfk_object_id', models.PositiveIntegerField()),
                ('gfk_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('tenant', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='tenant.Tenant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]