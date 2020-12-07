# Generated by Django 3.2 on 2020-12-07 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wowModel', '0002_auto_20201207_0616'),
    ]

    operations = [
        migrations.CreateModel(
            name='Corporation',
            fields=[
                ('corp_id', models.AutoField(primary_key=True, serialize=False)),
                ('corp_name', models.CharField(max_length=32)),
                ('corp_reg_num', models.CharField(max_length=20)),
                ('corp_discount', models.DecimalField(decimal_places=2, max_digits=3)),
            ],
            options={
                'db_table': 'corporation',
            },
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('coupon_id', models.DecimalField(decimal_places=0, max_digits=4, primary_key=True, serialize=False)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=4)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
            options={
                'db_table': 'coupon',
            },
        ),
        migrations.CreateModel(
            name='Indi_cust',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dl_num', models.CharField(max_length=15)),
                ('insur_com_name', models.CharField(max_length=32)),
                ('insur_polic_num', models.CharField(max_length=12)),
                ('coupon', models.ManyToManyField(blank=True, null=True, to='wowModel.Coupon')),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='wowModel.customer')),
            ],
            options={
                'db_table': 'indi_cust',
            },
        ),
        migrations.CreateModel(
            name='Corp_cust',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.DecimalField(decimal_places=0, max_digits=32)),
                ('corp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wowModel.corporation')),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='wowModel.customer')),
            ],
            options={
                'db_table': 'corp_cust',
            },
        ),
    ]