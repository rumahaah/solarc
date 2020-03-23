# Generated by Django 2.2.8 on 2020-01-13 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preproject', '0010_auto_20200113_0505'),
    ]

    operations = [
        migrations.CreateModel(
            name='Taxsonomi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(choices=[('0', 'Datacom'), ('1', 'Cloud'), ('2', 'Data Center'), ('3', 'Sec & Col'), ('4', 'ITO'), ('5', 'Insol'), ('6', 'Digital Ads')], max_length=1)),
            ],
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.AlterField(
            model_name='pre_project',
            name='taxsonomi',
            field=models.ManyToManyField(to='preproject.Taxsonomi'),
        ),
    ]
