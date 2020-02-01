# Generated by Django 2.2.7 on 2020-01-19 00:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20200119_0528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='emp_no',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(10000), django.core.validators.MinValueValidator(20000)]),
        ),
        migrations.AlterField(
            model_name='student',
            name='reg_no',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(10000), django.core.validators.MinValueValidator(20000)]),
        ),
    ]