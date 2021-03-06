# Generated by Django 3.0 on 2019-12-05 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('preproject', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Psapca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('psa_date', models.DateField()),
                ('pca_date', models.DateField(blank=True)),
                ('product_category', models.CharField(choices=[('d', 'Datacomm'), ('i', 'ITS')], max_length=1)),
                ('project_name', models.CharField(max_length=100)),
                ('productornot', models.CharField(choices=[('p', 'Product'), ('n', 'Non Product')], max_length=1)),
                ('scale', models.CharField(choices=[('s', 'Small'), ('m', 'Medium'), ('l', 'Large')], max_length=1)),
                ('summary', models.TextField(max_length=1000)),
                ('status', models.CharField(choices=[('g', 'GO'), ('h', 'HOLD'), ('n', 'NOT GO')], max_length=1)),
                ('remark', models.TextField(max_length=1000)),
                ('table_updated', models.DateField(auto_now=True)),
                ('table_creation_timestamp', models.DateField(auto_now_add=True)),
                ('customer', models.ManyToManyField(to='preproject.Customer')),
                ('pss_lintasarta', models.ManyToManyField(related_name='_psapca_pss_lintasarta_+', to='preproject.Lintasartaperson')),
                ('sales_lintasarta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='preproject.Lintasartaperson')),
            ],
        ),
    ]
