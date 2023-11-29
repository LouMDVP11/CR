from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from ..models import *
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError 
import json

# CRUD DE PROVINCE(Departamento)
class DonorView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self, request, id=0):
        if(id>0):
            donors=list(Donor.objects.select_related('idPerson').values())
            if len(donors) > 0:
                donor = donors[0]
                data={'message': "SUCCESS", "Donor" : donor}
            else:
                data={'message':'Donor not found...'}
        else:
            donors = Donor.objects.select_related('idPerson', 'idBloodType', 'idEthnicGroup', 'idCity').values(
                'id',
                'idPerson__id',
                'idBloodType__id',
                'idCity__id',
                'idEthnicGroup__id',
                'idPerson__firstName',
                'idPerson__lastName',
                'idPerson__gender',
                'idBloodType__bloodType',
                'idCity__city',
                'idEthnicGroup__ethnicGroup',
                'idPerson__email',
                'state',
                'donationAmount'
                ).order_by("id")
            if len(donors)>0:
                for donor in donors:
                    donor['Nombre(s)'] = donor['idPerson__firstName']
                    del donor['idPerson__firstName']
                    donor['Apellidos'] = donor['idPerson__lastName']
                    del donor['idPerson__lastName']
                    donor['Género'] = dict(Gender.choices).get(donor['idPerson__gender'])
                    del donor['idPerson__gender']
                    donor['Tipo de sangre'] = donor['idBloodType__bloodType']
                    del donor['idBloodType__bloodType']
                    donor['Municipio'] = donor['idCity__city']
                    del donor['idCity__city']
                    donor['Grupo étnico'] = donor['idEthnicGroup__ethnicGroup']
                    del donor['idEthnicGroup__ethnicGroup']
                    donor['Email'] = donor['idPerson__email']
                    del donor['idPerson__email']
                    donor['Cantidad de donaciones'] = donor['donationAmount']
                    del donor['donationAmount']
                    donor['EstadoDonador'] = dict(DonorState.choices).get(donor['state'])
                    del donor['state']
                    if donor['EstadoDonador']=="Elegible":
                        donor['Color']="success"
                    elif donor['EstadoDonador']=="Deshabilitado":
                        donor['Color']="error"
                    else:
                        donor['Color']="warning"
                    
                data={'message':"SUCCESS", "Donors":list(donors)}
            else:
                data={'message':'"Donors not found...', "Donors":[]}
        return JsonResponse(data)
    
    def post(self, request):
        jd = json.loads(request.body)
        #print(jd)
        try:
            person = Person.objects.get(id=jd['idPerson'])
            bloodType = BloodType.objects.get(id=jd['idBloodType_id'])
            ethnicGroup = EthnicGroup.objects.get(id=jd['idEthnicGroup'])
            city = City.objects.get(id=jd['idCity'])
            
            Donor.objects.create(homeAddress=jd['homeAddress'],workPhone=jd['workPhone'],workAddress=jd['workAddress'],birthPlace=jd['birthPlace'],state=jd['state'],stateDescription=jd['stateDescription'],donationAmount=jd['donationAmount'],lastDonationDate=jd['lastDonationDate'],homePhone=jd['homePhone'],idPerson=person,idBloodType=bloodType,idEthnicGroup=ethnicGroup,idCity=city)
            data={'message':'SUCCESS'}
            return JsonResponse(data)
        except IntegrityError:
            data = {
                "message": "ERROR",
            }
            return JsonResponse(data)
    
    def delete(self, id):
        donors=list(Donor.objects.filter(id=id).values())
        if donors>0:
            Donor.objects.filter(id=id).delete
            data={'message':"Donor deleted"}
        else:
            data={'message':"ERROR, donor not found"}
        return JsonResponse(data)
    
    def put(self,req,id):
        jd=json.loads(req.body)
        donors = list(Donor.objects.filter(id=id).values())
        if len(donors)>0:
            donor = Donor.objects.get(id=id)
            donor.nationality=jd['nationality']
            donor.homeAddress=jd['homeAddress']
            donor.homePhone=jd['homePhone']
            donor.workAddress=jd['workAddress']
            donor.workPhone=jd['workPhone']
            donor.birthPlace=jd['birthPlace']
            donor.state=jd['state']
            donor.stateDescription=jd['stateDescription']
            donor.donationAmount=jd['donationAmount']
            donor.lastDonationDate=jd['lastDonationDate']
            donor.idPerson=Person.objects.get(id=jd['id_person'])
            donor.idBloodType=BloodType.objects.get(id=jd['id_bloodType'])
            donor.idEthnicGroup=EthnicGroup.objects.get(id=jd['id_ethnicGroup'])
            donor.idCity=City.objects.get(id=jd['id_city'])
            donor.save()
            datos = {"message": "Donor successfully edited"}
        else:
            datos={"message": "Donor not found to edit"}
        return JsonResponse(datos)
    
class SuspendDonor(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, req, id):
        jd=json.loads(req.body)
        donors = list(Donor.objects.filter(id=id).values())
        if len(donors)>0:
            donor = Donor.objects.get(id=id)
            if donor.state != DonorState.SUSPENDED:
                donor.state = DonorState.SUSPENDED
                donor.stateDescription = jd['stateDescription']
                donor.save()
                data={"message":"Donador suspendido","reason":jd['stateDescription']}
            else:
                data={"message":"ERROR, Donador ya suspendido"}
        else:
            data={"message":"ERROR, donador no encontrado"}
        return JsonResponse(data)
    
class ActivateDonor(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, req, id):
        donors = list(Donor.objects.filter(id=id).values())
        if len(donors)>0:
            donor = Donor.objects.get(id=id)
            if donor.state != DonorState.ENABLED:
                donor.state = DonorState.ENABLED
                donor.stateDescription = ""
                donor.save()
                data={"message":"Donador activo"}
            else:
                data={"message":"ERROR, Donador ya activo"}
        else:
            data={"message":"ERROR, donador no encontrado"}
        return JsonResponse(data)

class SearchByPersonId(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(req,self,idPerson):
        if idPerson>0:
            donors = Donor.objects.filter(idPerson=idPerson).values()
            if len(donors)>0:
                data={'message':"SUCCESS", "Donors":list(donors)}
            else:
                data={'message':'"Donors not found...', "Donors":[]}
        return JsonResponse(data)  
    
class UpdateDonor(View):  
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
      
    def post(self,req,id):
        jd=json.loads(req.body)
        print(jd)
        donors = list(Donor.objects.filter(id=id).values())
        if len(donors)>0:
            donor = Donor.objects.get(id=id)
            donor.homeAddress=jd['homeAddress']
            donor.homePhone=jd['homePhone']
            donor.workAddress=jd['workAddress']
            donor.workPhone=jd['workPhone']
            donor.idBloodType=BloodType.objects.get(id=jd['idBloodType_id'])
            donor.idEthnicGroup=EthnicGroup.objects.get(id=jd['idEthnicGroup_id'])
            donor.idCity=City.objects.get(id=jd['idCity_id'])
            donor.save()
            datos = {"message": "Donor successfully edited"}
        else:
            datos={"message": "Donor not found to edit"}
        return JsonResponse(datos)
    
class UpdateBT(View):  

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
      
    def post(self,req,id):
        jd=json.loads(req.body)
        print(jd)
        donors = list(Donor.objects.filter(id=id).values())
        if len(donors)>0:
            donor = Donor.objects.get(id=id)
            donor.idBloodType=BloodType.objects.get(id=jd['idBloodType_id'])
            donor.save()
            datos = {"message": "SUCCESS"}
        else:
            datos={"message": "ERROR"}
        return JsonResponse(datos)
      
class UpdateBloodDonor(View):  
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
      
    def put(self,req,id):
            jd=json.loads(req.body)
            donors = list(Donor.objects.filter(id=id).values())
            if len(donors)>0:
                donor = Donor.objects.get(id=id)
                donor.idBloodType_id=jd['idBloodType']
                donor.save()
                datos = {"message": "Donor successfully edited"}
            else:
                datos={"message": "Donor not found to edit"}
            return JsonResponse(datos)

