# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DiningServer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Context',
            fields=[
                ('openid', models.CharField(verbose_name='用户OpenID', max_length=50, serialize=False, primary_key=True)),
                ('context_data', models.TextField(verbose_name='上下文对话数据')),
                ('expire_date', models.DateTimeField(db_index=True, verbose_name='过期日期')),
            ],
            options={
                'verbose_name': '微信上下文对话',
                'verbose_name_plural': '微信上下文对话',
                'db_table': 'wechat_context',
            },
        ),
    ]
