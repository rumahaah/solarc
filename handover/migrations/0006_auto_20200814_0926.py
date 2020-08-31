# Generated by Django 3.0.4 on 2020-08-14 02:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('psatopca', '0029_auto_20200810_1046'),
        ('handover', '0005_auto_20200602_1430'),
    ]

    operations = [
        migrations.CreateModel(
            name='CR_Overbudget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overbudget_category', models.CharField(choices=[('0', 'Customer CR Only'), ('1', 'Overbudget Only - Datacomm Problem On Desk Survey / Coverage'), ('2', 'Overbudget Only - Internal SA Problem'), ('3', 'Overbudget Only - SoW Problem'), ('4', 'Overbudget Only - Delivery Problem'), ('5', 'Overbudget Only - Kurs'), ('6', 'Customer CR to Overbudget - Increased Revenue - New Proposal Needed'), ('7', 'Customer CR to Overbudget - Decreased Revenue'), ('8', 'Customer CR to Overbudget - Absorbed Costs')], max_length=4)),
                ('remark', models.TextField(blank=True, max_length=1000, null=True)),
                ('bc_category_changes', models.CharField(choices=[('s', 'Same as before'), ('o', 'OpEx'), ('c', 'CapEx')], default='s', max_length=4)),
                ('ebitda_changes', models.DecimalField(decimal_places=2, max_digits=10)),
                ('irr_changes', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('tcv_changes_nominal', models.DecimalField(blank=True, decimal_places=2, max_digits=30, null=True)),
                ('pca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='psatopca.Pca')),
            ],
        ),
        migrations.AlterField(
            model_name='handover',
            name='problem_category',
            field=models.CharField(choices=[('n-pr', 'Clean - Fulfilled'), ('e-sc', 'External - Scope Change'), ('e-rn', 'External - Renewal Process'), ('e-po', 'External - Conduct PSA After PO'), ('e-pb', 'External - PO Backdate'), ('e-pr', 'External - Custom Product'), ('i-pc', 'Internal - PCA Approval'), ('i-de', 'Internal - Delay to HO')], default='n-pr', max_length=4),
        ),
        migrations.DeleteModel(
            name='Cleanproject',
        ),
    ]