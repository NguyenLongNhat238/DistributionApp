# Generated by Django 4.1.3 on 2023-05-08 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information_management', '0010_alter_employee_phone_alter_supplier_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='tax_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]