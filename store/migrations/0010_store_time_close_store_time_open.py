# Generated by Django 5.1.4 on 2025-06-26 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_order_assigned_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='time_close',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='store',
            name='time_open',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
