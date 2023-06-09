# Generated by Django 4.2.1 on 2023-07-05 07:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('information_management', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='channel',
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=50, null=True, verbose_name='Code')),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=50, verbose_name='Status')),
                ('slug', models.SlugField(blank=True, default=uuid.uuid4, editable=False, max_length=250, unique=True, verbose_name='Slug')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('name', models.CharField(max_length=100, verbose_name='Channel name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('company', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_company_related', related_query_name='%(app_label)s_%(class)s_company', to='information_management.company', verbose_name='Company')),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_created_by_related', related_query_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('updated_by', models.ForeignKey(blank=True, db_constraint=False, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='%(app_label)s_%(class)s_updated_by_related', related_query_name='%(app_label)s_%(class)s_updated_by', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
            ],
        ),
        migrations.AddConstraint(
            model_name='channel',
            constraint=models.UniqueConstraint(fields=('code', 'company'), name='unique_code_company_channel'),
        ),
        migrations.AddConstraint(
            model_name='channel',
            constraint=models.UniqueConstraint(fields=('name', 'company'), name='unique_channel_name_company'),
        ),
    ]
