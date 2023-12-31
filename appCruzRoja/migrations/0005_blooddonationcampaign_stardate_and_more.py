# Generated by Django 4.2.5 on 2023-11-11 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appCruzRoja', '0004_alter_personaldonation_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='blooddonationcampaign',
            name='starDate',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='personaldonation',
            name='state',
            field=models.IntegerField(choices=[(1, 'Aprobada'), (2, 'En espera'), (3, 'Rechazada'), (4, 'Cancelada')], default=2),
        ),
    ]
