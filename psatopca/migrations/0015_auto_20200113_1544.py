# Generated by Django 2.2.8 on 2020-01-13 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psatopca', '0014_psa_pss_ho_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='psa',
            name='pss_ho_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
