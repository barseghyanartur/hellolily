# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-21 14:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email', '0037_emailaccount_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailmessage',
            name='is_inbox_message',
            field=models.NullBooleanField(db_index=True, verbose_name='Is inbox'),
        ),
        migrations.AddField(
            model_name='emailmessage',
            name='is_sent_message',
            field=models.NullBooleanField(db_index=True, verbose_name='Is sent'),
        ),
        migrations.AddField(
            model_name='emailmessage',
            name='is_spam_message',
            field=models.NullBooleanField(db_index=True, verbose_name='Is spam'),
        ),
        migrations.AddField(
            model_name='emailmessage',
            name='is_trashed_message',
            field=models.NullBooleanField(db_index=True, verbose_name='Is trashed'),
        ),
        migrations.AddField(
            model_name='emailmessage',
            name='is_draft_message',
            field=models.NullBooleanField(db_index=True, verbose_name='Is draft'),
        ),
        migrations.AddField(
            model_name='emailmessage',
            name='is_starred_message',
            field=models.NullBooleanField(db_index=True, verbose_name='Is starred'),
        ),
    ]