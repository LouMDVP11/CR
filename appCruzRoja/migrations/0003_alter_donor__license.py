# Generated by Django 4.2.4 on 2023-11-05 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appCruzRoja', '0002_receiver_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donor',
            name='_license',
            field=models.CharField(max_length=25, null=True),
        ),
    ]