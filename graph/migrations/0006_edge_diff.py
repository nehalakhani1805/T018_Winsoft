# Generated by Django 3.1.1 on 2020-09-27 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graph', '0005_auto_20200926_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='edge',
            name='diff',
            field=models.IntegerField(default=0),
        ),
    ]
