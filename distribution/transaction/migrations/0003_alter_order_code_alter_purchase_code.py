# Generated by Django 4.1.3 on 2023-05-04 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_alter_orderdetail_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='code',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='code',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='Code'),
        ),
    ]
