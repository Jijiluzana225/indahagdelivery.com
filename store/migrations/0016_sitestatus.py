# Generated by Django 5.0.4 on 2025-07-24 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_remove_customerprofile_facebook_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Open', 'Open'), ('Closed', 'Closed'), ('Weekend', 'Weekend')], default='Closed', max_length=20, null=True)),
            ],
        ),
    ]
