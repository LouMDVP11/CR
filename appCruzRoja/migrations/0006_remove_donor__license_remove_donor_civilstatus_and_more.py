# Generated by Django 4.1.1 on 2023-11-12 04:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appCruzRoja', '0005_blooddonationcampaign_stardate_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donor',
            name='_license',
        ),
        migrations.RemoveField(
            model_name='donor',
            name='civilStatus',
        ),
        migrations.RemoveField(
            model_name='donor',
            name='nationality',
        ),
        migrations.RemoveField(
            model_name='donor',
            name='ocupation',
        ),
        migrations.RemoveField(
            model_name='donor',
            name='passport',
        ),
    ]
