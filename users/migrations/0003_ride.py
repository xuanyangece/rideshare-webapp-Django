# Generated by Django 2.1.5 on 2019-01-29 03:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190129_0044'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='open', max_length=10)),
                ('destination', models.CharField(max_length=50)),
                ('arrivaldate', models.DateTimeField()),
                ('passenger', models.IntegerField(validators=[django.core.validators.MaxValueValidator(200), django.core.validators.MinValueValidator(1)])),
                ('sharable', models.BooleanField(default=False)),
                ('vehicle', models.CharField(max_length=20)),
                ('special', models.CharField(max_length=200)),
                ('users', models.ManyToManyField(to='users.UserProfile')),
            ],
        ),
    ]
