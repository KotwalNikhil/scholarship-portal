# Generated by Django 2.2.7 on 2020-06-06 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_profile_attendence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='father_rank',
            field=models.CharField(choices=[('Lance Naik', 'Lance Naik'), ('Naik', 'Naik'), ('Hawaldar', 'Hawaldar'), ('Nb Subedar', 'Nb Subedar'), ('Subedar', 'Subedar'), ('Subeder Maj', 'Subeder Maj'), ('Officer', 'Officer')], default='Officer', max_length=50),
        ),
    ]
