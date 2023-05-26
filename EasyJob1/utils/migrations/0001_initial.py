# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-05-17 04:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pos_no', models.IntegerField(default=0)),
                ('uno', models.IntegerField(default=0)),
                ('date', models.DateField()),
                ('state', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Areas',
            fields=[
                ('id', models.AutoField(default=0, primary_key=True, serialize=False)),
                ('code', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=50)),
                ('cno', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Careertalk',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.IntegerField()),
                ('loc', models.CharField(max_length=128)),
                ('desc', models.TextField()),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.AutoField(default=0, primary_key=True, serialize=False)),
                ('code', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=50)),
                ('pno', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=50, null=True)),
                ('boss', models.CharField(max_length=50, null=True)),
                ('reg_l', models.CharField(max_length=50, null=True)),
                ('reg_d', models.DateField()),
                ('state', models.CharField(max_length=20)),
                ('loc', models.CharField(max_length=50, null=True)),
                ('phone', models.CharField(max_length=50, null=True)),
                ('emill', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Industy',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('pre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pos_no', models.IntegerField(default=0)),
                ('uno', models.IntegerField(default=0)),
                ('date', models.DateField()),
                ('state', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Job_Intention',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=20)),
                ('salary', models.IntegerField(default=0)),
                ('loc', models.IntegerField(default=0)),
                ('industryno', models.IntegerField(default=0)),
                ('uno', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Jobseeker',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('sex', models.CharField(max_length=20)),
                ('loc', models.CharField(max_length=50)),
                ('polistatus', models.CharField(max_length=20)),
                ('birth', models.DateField()),
                ('grad', models.IntegerField(default=0)),
                ('phone', models.CharField(max_length=50)),
                ('emill', models.EmailField(max_length=254)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('type', models.IntegerField(default=0)),
                ('state', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('compno', models.IntegerField(default=0)),
                ('indus', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=50)),
                ('grad', models.IntegerField(default=0)),
                ('salary', models.IntegerField(default=0)),
                ('desc', models.TextField()),
                ('loc', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Provinces',
            fields=[
                ('id', models.AutoField(default=0, primary_key=True, serialize=False)),
                ('code', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('loc', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='sysinfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('userid', models.IntegerField()),
                ('key', models.CharField(max_length=20)),
                ('value', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Xueli',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first', models.DateField()),
                ('end', models.DateField()),
                ('sno', models.IntegerField(default=0)),
                ('type', models.IntegerField(default=0)),
                ('uid', models.IntegerField(default=0)),
            ],
        ),
    ]
