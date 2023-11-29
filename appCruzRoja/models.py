from django.db import models
from django.contrib.postgres.fields import ArrayField

#--------------------------------CHOICES----------------------------------
class DonorState(models.IntegerChoices):
    DISABLED = 0,'Deshabilitado'
    ENABLED = 1,'Elegible'
    SUSPENDED = 2,'No elegible'
class EmployeeState(models.IntegerChoices):
    DISABLED = 3,'Desactivo'
    ENABLED = 1,'Activado'
    SUSPENDED = 2,'Suspendido'
class ReceptorState(models.IntegerChoices):
    DISABLED = 2,'Desactivo'
    ENABLED = 1,'Activado'

class Gender(models.IntegerChoices):
    MASCULINE = 0, 'Masculino'
    FEMENINE = 1, 'Femenino'
    OTHER = 2, 'Otro'
    
class UserType(models.IntegerChoices):
    DONOR = 0, 'Donante'
    EMPLOYEE = 1, 'Empleado'
    DONOR_AND_EMPLOYEE = 2, 'Donante y empleado'

class DonationState(models.IntegerChoices):
    FULL = 1,'Completa'
    HALF = 2,'Incompleta'
    BDC_NULL = 3,'Diferido'
    IN_PROCESS = 4,'En proceso'
 
class BloodDonationCampaignState(models.IntegerChoices):
    FINISHED = 1,'Finalizada'
    WAITING = 2,'En espera'
    IN_PROCESS = 3,'En proceso'
    CANCELED = 4,'Cancelada' 
class PersonalDonationState(models.IntegerChoices):
    APROVED = 1,'Aprobada'
    WAITING = 2,'En espera'
    REJECTED = 3,'Rechazada'
    CANCEL = 4,'Cancelada'
class PostPriority(models.IntegerChoices):
    EMERGENCY = 1,'Emergencia'
    HIGH = 2,'Alta'
    MEDIUM = 3,'Media'
    LOW = 4,'Baja'
class CampaignReceiverPurpose(models.IntegerChoices):
    INDIVIDUAL = 1,'Individual'
    SESSION = 2,'Jornada'
    BLEEDING = 3,'Sangría'
#-----------------------------------------------MODELS--------------------------------------
class Province(models.Model):
    province=models.CharField(max_length=20)
    
class Motive(models.Model):
    motive=models.CharField(max_length=20)
    suspendedTime=models.IntegerField()
    
class BloodType(models.Model):
    bloodType=models.CharField(max_length=4)
    
class EthnicGroup(models.Model):
    ethnicGroup=models.CharField(max_length=20)
    
class DonationType(models.Model):
    donationType=models.CharField(max_length=15)
    
class Position(models.Model):
    position=models.CharField(max_length=50)
    description=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
class City(models.Model):
    city=models.CharField(max_length=30)
    idProvince=models.ForeignKey(Province, on_delete=models.CASCADE)
    
class Receiver(models.Model):
    receiverName=models.CharField(max_length=150, unique=True)
    address=models.CharField(max_length=150)
    telephone=models.CharField(max_length=15, null=True)
    state=models.IntegerField(default=ReceptorState.ENABLED, choices=ReceptorState.choices)
    email=models.CharField(max_length=80, null=True)
    observations=models.CharField(max_length=200, null=True)
    dpiPatient=models.CharField(max_length=13, null=True, unique=True)
    idExtranjero=models.CharField(max_length=20, null=True, unique=True)
    idCity=models.ForeignKey(City, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
class Person(models.Model):
    dpi=models.CharField(max_length=13, unique=True, null=True)
    idExtranjero=models.CharField(max_length=20, unique=True, null=True)
    firstName=models.CharField(max_length=50)
    lastName=models.CharField(max_length=50)
    user=models.CharField(max_length=20, null=True)
    _password=models.CharField(max_length=500, null=True)
    email=models.CharField(max_length=80, null=True)
    gender=models.IntegerField(default=Gender.MASCULINE, choices=Gender.choices)
    birthDate=models.DateField()
    userType=models.IntegerField(default=UserType.DONOR, choices=UserType.choices)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
class Employee(models.Model):
    idPerson=models.ForeignKey(Person, on_delete=models.CASCADE, unique=True)
    idPosition=models.ForeignKey(Position, on_delete=models.CASCADE)
    rol=models.IntegerField(default=1)
    state=models.IntegerField(default=EmployeeState.ENABLED, choices=EmployeeState.choices)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
class Donor(models.Model):
    homeAddress=models.CharField(max_length=150,null=True)
    homePhone=models.CharField(max_length=20,null=True)
    workAddress=models.CharField(max_length=150, null=True)
    workPhone=models.CharField(max_length=20,null=True)
    birthPlace=models.CharField(max_length=200,null=True)
    state=models.IntegerField(default=DonorState.ENABLED, choices=DonorState.choices)
    stateDescription=models.CharField(max_length=250,null=True)
    donationAmount=models.IntegerField()
    lastDonationDate=models.DateField(null = True)
    idPerson=models.ForeignKey(Person, on_delete=models.CASCADE, unique=True)
    idBloodType=models.ForeignKey(BloodType, on_delete=models.CASCADE)
    idEthnicGroup=models.ForeignKey(EthnicGroup, on_delete=models.CASCADE)
    idCity=models.ForeignKey(City, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
class BloodDonationCampaign(models.Model):
    _date=models.DateField(null=True)
    starDate=models.DateTimeField(null=True)
    place=models.CharField(max_length=150, null=True)
    state=models.IntegerField(default=BloodDonationCampaignState.WAITING, choices=BloodDonationCampaignState.choices)
    observations=models.CharField(max_length=200,null=True)
    bloodUnitsCollected=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
class CampaignReceiver(models.Model):
    bloodUnitsReceived=models.IntegerField()
    purpose=models.IntegerField(default=CampaignReceiverPurpose.SESSION, choices=CampaignReceiverPurpose.choices)
    idReceiver=models.ForeignKey(Receiver, on_delete=models.CASCADE)
    idBloodDonationCampaign=models.ForeignKey(BloodDonationCampaign, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
class Donation(models.Model):
    correlative=models.IntegerField(null=True)
    bloodCorrelative=models.CharField(max_length=20,null=True)
    state=models.IntegerField(default=DonationState.IN_PROCESS, choices=DonationState.choices)
    comments=models.CharField(max_length=200, null=True)
    weight=models.FloatField(null=True)
    temperature=models.FloatField(null=True)
    bloodPressure=models.FloatField(null=True)
    hemoglobin=models.FloatField(null=True)
    idDonationType=models.ForeignKey(DonationType, on_delete=models.CASCADE)
    idBloodDonationCampaign=models.ForeignKey(BloodDonationCampaign, on_delete=models.CASCADE)
    idDonor=models.ForeignKey(Donor, on_delete=models.CASCADE)
    asignado=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class DonationReceiverCampaign(models.Model):
    idDonation=models.ForeignKey(Donation, on_delete=models.CASCADE)
    idReceiverCampaign=models.ForeignKey(CampaignReceiver, on_delete=models.CASCADE, )
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class CampaignBloodType(models.Model):
    idCampaignReceiver=models.ForeignKey(CampaignReceiver, on_delete=models.CASCADE)
    idBloodType=models.ForeignKey(BloodType, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class PersonalDonation(models.Model):
    _date=models.DateField()
    _image=models.TextField()
    description=models.CharField(max_length=400, null=True)
    state=models.IntegerField(default=PersonalDonationState.WAITING, choices=PersonalDonationState.choices)
    idDonor=models.ForeignKey(Donor, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
class Achievement(models.Model):
    name=models.CharField(max_length=50, null=True)
    description=models.CharField(max_length=200, null=True)
    icon=models.ImageField(null=True, upload_to='media/', max_length=500)
    amount= models.IntegerField()
    duration= models.IntegerField(null = True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
class DonorAchievement(models.Model):
    aquisitionDate=models.DateField(auto_now_add=True)
    idAchievement=models.ForeignKey(Achievement, on_delete=models.CASCADE)
    idDonor=models.ForeignKey(Donor, on_delete=models.CASCADE, default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Publication(models.Model):

    title=models.CharField(max_length=300, null=True) 
    expirationDate=models.DateField(null=True)
    _priority=models.IntegerField(default=PostPriority.MEDIUM, choices=PostPriority.choices)
    _content=models.CharField(max_length=600, null=True)
    multimedia=models.ImageField(upload_to='media/', max_length=500, null=True)
    idEmployee=models.ForeignKey(Employee, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
class DonationLog(models.Model):
    description=models.CharField(max_length=250, null=True)
    idDonation=models.ForeignKey(Donation, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class PublicationLog(models.Model):
    description=models.CharField(max_length=1000, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class BloodDonationCampaingLog(models.Model):
    description=models.CharField(max_length=250, null=True)
    idBloodDonationCampaign=models.ForeignKey(BloodDonationCampaign, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class DonorSuspendedLog(models.Model):
    initialDate=models.DateField()
    finalDate=models.DateField()
    idDonor=models.ForeignKey(Donor, on_delete=models.CASCADE)
    idMotive=models.ForeignKey(Motive, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

#  COMMENT