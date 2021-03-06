# Generated by Django 2.2.7 on 2020-02-27 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0003_auto_20200113_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholarship',
            name='document',
            field=models.FileField(upload_to='documents/scholarship_broucher/'),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='img',
            field=models.ImageField(default='pics/scholarship_pics/default.png', upload_to='pics'),
        ),
    ]
