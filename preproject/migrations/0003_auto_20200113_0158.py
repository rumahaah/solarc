# Generated by Django 2.2.8 on 2020-01-13 01:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('preproject', '0002_auto_20200113_0155'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pre_project',
            old_name='customer',
            new_name='opportunity',
        ),
    ]
