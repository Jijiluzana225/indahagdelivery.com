# Generated by Django 5.1.4 on 2025-06-24 06:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_order_assigned_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='assigned_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.deliverydriver'),
        ),
    ]
