# Generated by Django 2.2.7 on 2020-09-07 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0018_auto_20200907_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholarship',
            name='scholarship_form',
            field=models.FileField(default='documents/scholarship_form/default_scholarship_form.png', upload_to='documents/scholarship_form/'),
        ),
    ]
