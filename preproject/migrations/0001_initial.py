# Generated by Django 3.0 on 2019-12-05 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100)),
                ('customersegment', models.CharField(choices=[('0', 'Banking 1'), ('1', 'Banking 2'), ('2', 'Finance Non-Bank'), ('3', 'Supply Chain'), ('4', 'Public Sector 1'), ('5', 'Public Sector 2'), ('6', 'Resources'), ('7', 'Telco')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Lintasartaperson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initial', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Pre_project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=100)),
                ('opportunity_id', models.CharField(max_length=20)),
                ('remark', models.TextField(max_length=1000)),
                ('issues', models.TextField(max_length=1000)),
                ('project_status', models.CharField(choices=[('c', 'Create'), ('o', 'Open'), ('b', 'Break')], max_length=1)),
                ('solution_criteria', models.CharField(choices=[('s', 'Standard'), ('m', 'Multiservice'), ('c', 'Complex')], max_length=1)),
                ('key_strategic_account', models.BooleanField(default=False)),
                ('progress', models.CharField(choices=[('w', 'Close Won'), ('l', 'Close Lost'), ('p', 'Progress'), ('c', 'Cancelled')], max_length=1)),
                ('product', models.CharField(choices=[('c', 'Connectivity'), ('i', 'ITS')], max_length=1)),
                ('payment', models.CharField(choices=[('m', 'MRC'), ('o', 'OTC')], max_length=1)),
                ('table_updated', models.DateField(auto_now=True)),
                ('table_creation_timestamp', models.DateField(auto_now_add=True)),
                ('customer', models.ManyToManyField(to='preproject.Customer')),
                ('pss_lintasarta', models.ManyToManyField(related_name='pss_lintasarta', to='preproject.Lintasartaperson')),
                ('sa_lintasarta', models.ManyToManyField(related_name='sa_lintasarta', to='preproject.Lintasartaperson')),
                ('sales_lintasarta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_lintasarta', to='preproject.Lintasartaperson')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(choices=[('0', 'Datacom'), ('1', 'Cloud'), ('2', 'Data Center'), ('3', 'Sec & Col'), ('4', 'ITO'), ('5', 'Insol'), ('6', 'Digigal Ads')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='PSA_PCA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('psa_date', models.DateField()),
                ('pca_date', models.DateField()),
                ('remark', models.TextField(max_length=1000)),
                ('issues', models.TextField(max_length=1000)),
                ('table_updated', models.DateField(auto_now=True)),
                ('table_creation_timestamp', models.DateField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preproject.Pre_project')),
            ],
        ),
        migrations.AddField(
            model_name='pre_project',
            name='taxsonomi',
            field=models.ManyToManyField(to='preproject.Product'),
        ),
    ]
