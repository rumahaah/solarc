# Generated by Django 2.2.8 on 2020-01-13 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preproject', '0007_auto_20200113_0456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customercriteria',
            field=models.CharField(choices=[('0', 'Key Strategic Account'), ('1', 'Emerging Account'), ('2', 'Strategic Account')], max_length=3),
        ),
    ]
