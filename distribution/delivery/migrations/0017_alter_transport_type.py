# Generated by Django 4.1.3 on 2023-05-09 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0016_alter_delivery_delivery_status_alter_transport_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transport',
            name='type',
            field=models.CharField(choices=[('truck', 'TRUCK'), ('motobike', 'MOTOBIKE'), ('car', 'CAR')], default='CAR', max_length=50),
        ),
    ]