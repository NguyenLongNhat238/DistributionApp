# Generated by Django 4.1.3 on 2023-05-15 15:33

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_alter_category_name_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='category',
            managers=[
                ('company_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='inventory',
            managers=[
                ('company_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='measurementunit',
            managers=[
                ('company_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='product',
            managers=[
                ('company_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='warehouse',
            managers=[
                ('company_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]