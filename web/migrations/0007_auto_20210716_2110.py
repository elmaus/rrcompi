# Generated by Django 3.1.1 on 2021-07-16 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_remove_rruser_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='rruser',
            name='title',
            field=models.CharField(choices=[('member', 'member'), ('judge', 'judge'), ('staff', 'staff'), ('pending', 'pending')], default='Pending', max_length=50),
        ),
        migrations.AlterField(
            model_name='rruser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='rruser',
            name='is_staff',
            field=models.BooleanField(default=True),
        ),
    ]
