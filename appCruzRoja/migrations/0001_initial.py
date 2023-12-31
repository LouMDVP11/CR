# Generated by Django 4.2.4 on 2023-11-09 21:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('description', models.CharField(max_length=200, null=True)),
                ('icon', models.ImageField(max_length=500, null=True, upload_to='media/')),
                ('amount', models.IntegerField()),
                ('duration', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='BloodDonationCampaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_date', models.DateField(null=True)),
                ('place', models.CharField(max_length=150, null=True)),
                ('state', models.IntegerField(choices=[(1, 'Finalizada'), (2, 'En espera'), (3, 'En proceso'), (4, 'Cancelada')], default=2)),
                ('observations', models.CharField(max_length=200, null=True)),
                ('bloodUnitsCollected', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='BloodType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bloodType', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='CampaignReceiver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bloodUnitsReceived', models.IntegerField()),
                ('purpose', models.IntegerField(choices=[(1, 'Individual'), (2, 'Jornada'), (3, 'Sangría')], default=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('idBloodDonationCampaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCruzRoja.blooddonationcampaign')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correlative', models.IntegerField(null=True)),
                ('bloodCorrelative', models.CharField(max_length=20, null=True)),
                ('state', models.IntegerField(choices=[(1, 'Completa'), (2, 'Incompleta'), (3, 'Autoexclusion'), (4, 'En proceso')], default=4)),
                ('comments', models.CharField(max_length=200, null=True)),
                ('weight', models.FloatField(null=True)),
                ('temperature', models.FloatField(null=True)),
                ('bloodPressure', models.FloatField(null=True)),
                ('hemoglobin', models.FloatField(null=True)),
                ('asignado', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('idBloodDonationCampaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCruzRoja.blooddonationcampaign')),
            ],
        ),
        migrations.CreateModel(
            name='DonationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('donationType', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_license', models.CharField(max_length=25, null=True)),
                ('passport', models.CharField(max_length=25, null=True)),
                ('nationality', models.CharField(max_length=50, null=True)),
                ('civilStatus', models.IntegerField(choices=[(0, 'Casado(a)'), (1, 'Soltero(a)')], default=1)),
                ('ocupation', models.CharField(max_length=50, null=True)),
                ('homeAddress', models.CharField(max_length=150, null=True)),
                ('homePhone', models.CharField(max_length=20, null=True)),
                ('workAddress', models.CharField(max_length=150, null=True)),
                ('workPhone', models.CharField(max_length=20, null=True)),
                ('birthPlace', models.CharField(max_length=200, null=True)),
                ('state', models.IntegerField(choices=[(0, 'Deshabilitado'), (1, 'Elegible'), (2, 'No elegible')], default=1)),
                ('stateDescription', models.CharField(max_length=250, null=True)),
                ('donationAmount', models.IntegerField()),
                ('lastDonationDate', models.DateField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('idBloodType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCruzRoja.bloodtype')),
                ('idCity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCruzRoja.city')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField(choices=[(3, 'Desactivo'), (1, 'Activado'), (2, 'Suspendido')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EthnicGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ethnicGroup', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Motive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motive', models.CharField(max_length=20)),
                ('suspendedTime', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dpi', models.CharField(max_length=13, null=True, unique=True)),
                ('idExtranjero', models.CharField(max_length=20, null=True, unique=True)),
                ('firstName', models.CharField(max_length=50)),
                ('lastName', models.CharField(max_length=50)),
                ('user', models.CharField(max_length=20, null=True)),
                ('_password', models.CharField(max_length=500, null=True)),
                ('email', models.CharField(max_length=80, null=True)),
                ('gender', models.IntegerField(choices=[(0, 'Masculino'), (1, 'Femenino'), (2, 'Otro')], default=0)),
                ('birthDate', models.DateField()),
                ('userType', models.IntegerField(choices=[(0, 'Donante'), (1, 'Empleado'), (2, 'Donante y empleado')], default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PublicationLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=1000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Receiver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiverName', models.CharField(max_length=150, unique=True)),
                ('address', models.CharField(max_length=150)),
                ('telephone', models.CharField(max_length=15, null=True)),
                ('state', models.IntegerField(choices=[(2, 'Desactivo'), (1, 'Activado')], default=1)),
                ('email', models.CharField(max_length=80, null=True)),
                ('observations', models.CharField(max_length=200, null=True)),
                ('dpiPatient', models.CharField(max_length=13, null=True, unique=True)),
                ('idExtranjero', models.CharField(max_length=20, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('idCity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCruzRoja.city')),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, null=True)),
                ('expirationDate', models.DateField(null=True)),
                ('_priority', models.IntegerField(choices=[(1, 'Emergencia'), (2, 'Alta'), (3, 'Media'), (4, 'Baja')], default=3)),
                ('_content', models.CharField(max_length=600, null=True)),
                ('multimedia', models.ImageField(max_length=500, null=True, upload_to='media/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('idEmployee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCruzRoja.employee')),
            ],
        ),
        migrations.CreateModel(
            name='PersonalDonation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_date', models.DateField()),
                ('_image', models.TextField()),
                ('description', models.CharField(max_length=400, null=True)),
                ('state', models.IntegerField(choices=[(1, 'Aprobada'), (2, 'En espera'), (3, 'Rechazada'), (4, 'Cancelada')], default=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('idDonor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCruzRoja.donor')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='idPerson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCruzRoja.person', unique=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='idPosition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCruzRoja.position'),
        ),
        migrations.CreateModel(
            name='DonorSuspendedLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initialDate', models.DateField()),
                ('finalDate', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('idDonor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCruzRoja.donor')),
                ('idMotive', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCruzRoja.motive')),
            ],
        ),
        migrations.CreateModel(
            name='DonorAchievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aquisitionDate', models.DateField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('idAchievement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCruzRoja.achievement')),
                ('idDonor', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='appCruzRoja.donor')),
            ],
        ),
        migrations.AddField(
            model_name='donor',
            name='idEthnicGroup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCruzRoja.ethnicgroup'),
        ),
        migrations.AddField(
            model_name='donor',
            name='idPerson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCruzRoja.person', unique=True),
        ),
        migrations.CreateModel(
            name='DonationReceiverCampaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('idDonation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCruzRoja.donation')),
                ('idReceiverCampaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCruzRoja.campaignreceiver')),
            ],
        ),
        migrations.CreateModel(
            name='DonationLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('idDonation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCruzRoja.donation')),
            ],
        ),
        migrations.AddField(
            model_name='donation',
            name='idDonationType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCruzRoja.donationtype'),
        ),
        migrations.AddField(
            model_name='donation',
            name='idDonor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCruzRoja.donor'),
        ),
        migrations.AddField(
            model_name='city',
            name='idProvince',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCruzRoja.province'),
        ),
        migrations.AddField(
            model_name='campaignreceiver',
            name='idReceiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCruzRoja.receiver'),
        ),
        migrations.CreateModel(
            name='CampaignBloodType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('idBloodType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCruzRoja.bloodtype')),
                ('idCampaignReceiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCruzRoja.campaignreceiver')),
            ],
        ),
        migrations.CreateModel(
            name='BloodDonationCampaingLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('idBloodDonationCampaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCruzRoja.blooddonationcampaign')),
            ],
        ),
    ]
