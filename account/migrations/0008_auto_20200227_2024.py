# Generated by Django 2.2.7 on 2020-02-27 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20200221_1117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='reg_no',
        ),
        migrations.AddField(
            model_name='profile',
            name='branch',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='division',
            field=models.IntegerField(default=0),
        ),
    ]
