# Generated by Django 2.1.5 on 2019-01-30 01:54

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190130_0152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='sharer_id',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=[], size=None),
        ),
    ]
