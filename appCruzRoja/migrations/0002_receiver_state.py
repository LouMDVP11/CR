# Generated by Django 4.2.5 on 2023-11-04 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appCruzRoja', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiver',
            name='state',
            field=models.IntegerField(choices=[(2, 'Desactivo'), (1, 'Activado')], default=1),
        ),
    ]
