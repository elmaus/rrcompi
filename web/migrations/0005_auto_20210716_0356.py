# Generated by Django 3.1.1 on 2021-07-16 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20210714_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rruser',
            name='title',
            field=models.CharField(choices=[('member', 'member'), ('judge', 'judge'), ('staff', 'staff'), ('pending', 'pending')], default='Pending', max_length=50),
        ),
    ]