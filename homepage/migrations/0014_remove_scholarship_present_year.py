# Generated by Django 2.2.7 on 2020-07-31 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0013_scholarship_present_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scholarship',
            name='present_year',
        ),
    ]
