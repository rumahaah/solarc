# Generated by Django 3.0.4 on 2020-06-02 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preproject', '0036_auto_20200514_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preproject',
            name='pss_lintasarta',
            field=models.ManyToManyField(to='preproject.Pssperson'),
        ),
    ]