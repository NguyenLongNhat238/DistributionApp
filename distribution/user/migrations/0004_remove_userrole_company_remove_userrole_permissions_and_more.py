# Generated by Django 4.2.1 on 2023-06-28 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system_admin', '0001_initial'),
        ('user', '0003_user_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userrole',
            name='company',
        ),
        migrations.RemoveField(
            model_name='userrole',
            name='permissions',
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_role_related', related_query_name='user_role', to='system_admin.userrole'),
        ),
        migrations.DeleteModel(
            name='Permission',
        ),
        migrations.DeleteModel(
            name='UserRole',
        ),
    ]
