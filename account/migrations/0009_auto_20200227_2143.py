# Generated by Django 2.2.7 on 2020-02-27 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20200227_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='pics/profile_pics/default.png', upload_to='pics/profile_pics'),
        ),
    ]
