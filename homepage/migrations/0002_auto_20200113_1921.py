# Generated by Django 2.2.7 on 2020-01-13 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholarship',
            name='img',
            field=models.ImageField(default='default.png', upload_to='pics'),
        ),
    ]