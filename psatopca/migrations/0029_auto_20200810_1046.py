# Generated by Django 3.0.4 on 2020-08-10 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psatopca', '0028_auto_20200514_2050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pca',
            name='flagcalc',
        ),
        migrations.AddField(
            model_name='pca',
            name='bc_category',
            field=models.CharField(choices=[('o', 'OpEx'), ('c', 'CapEx'), ('e', 'Exclude')], default='o', max_length=4),
            preserve_default=False,
        ),
    ]