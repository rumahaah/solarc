# Generated by Django 2.2.8 on 2020-01-27 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preproject', '0027_auto_20200127_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preproject',
            name='sa_lintasarta',
            field=models.ManyToManyField(to='preproject.Saperson'),
        ),
    ]
