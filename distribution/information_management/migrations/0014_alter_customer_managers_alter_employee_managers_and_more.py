# Generated by Django 4.1.3 on 2023-05-15 15:33

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('information_management', '0013_alter_supplier_name'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customer',
            managers=[
                ('company_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='employee',
            managers=[
                ('company_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='supplier',
            managers=[
                ('company_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
