# Generated by Django 3.0.4 on 2020-08-14 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preproject', '0035_auto_20200508_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_criteria',
            field=models.CharField(choices=[('0', 'Strategic Key Account'), ('1', 'Emerging Account'), ('2', 'Key Account'), ('3', 'New Customer & Not EA'), ('4', 'Regular Account')], max_length=1),
        ),
        migrations.AlterField(
            model_name='preproject',
            name='payment',
            field=models.CharField(choices=[('m', 'MRC'), ('o', 'OTC'), ('a', 'OTC & MRC')], max_length=1),
        ),
    ]
