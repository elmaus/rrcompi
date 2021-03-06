# Generated by Django 3.1.1 on 2021-07-15 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contender',
            name='password',
        ),
        migrations.RemoveField(
            model_name='contender',
            name='competition',
        ),
        migrations.AddField(
            model_name='contender',
            name='competition',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='compi.competition'),
        ),
        migrations.AlterField(
            model_name='criteria',
            name='competition',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='compi.competition'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='link',
            field=models.URLField(),
        ),
    ]
