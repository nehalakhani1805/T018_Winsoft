# Generated by Django 3.1.1 on 2020-09-26 13:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('graph', '0004_edge_vertex'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vertex',
            options={'verbose_name_plural': 'Vertices'},
        ),
        migrations.AlterField(
            model_name='input',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
