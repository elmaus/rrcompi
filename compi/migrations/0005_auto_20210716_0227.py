# Generated by Django 3.1.1 on 2021-07-15 23:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compi', '0004_auto_20210715_2121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='judge',
            name='competitions',
        ),
        migrations.AddField(
            model_name='judge',
            name='competition',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='compi.competition'),
        ),
    ]
