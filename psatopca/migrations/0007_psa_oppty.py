# Generated by Django 2.2.8 on 2020-01-13 02:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('preproject', '0003_auto_20200113_0158'),
        ('psatopca', '0006_auto_20200113_0155'),
    ]

    operations = [
        migrations.AddField(
            model_name='psa',
            name='oppty',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='preproject.Pre_project'),
            preserve_default=False,
        ),
    ]
