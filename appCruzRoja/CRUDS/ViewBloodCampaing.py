from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from ..models import *
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt 
import json
from django.db.models import F
import pytz
from datetime import datetime, date
#------------------------------------------------ CRUD Campaign---------------------------------------------------------
class BloodDonationCampaignView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self, request, id=0):
        if(id>0):
            listBloodDonationCampaign=(BloodDonationCampaign.objects.select_related().filter(id=id).values(
                    Id= F("id"),
                    Fecha= F("_date"),
                    FechaInicio = F("starDate"),
                    Lugar= F("place"),
                    Estado= F("state"),
                    Observaciones = F("observations"),
                    Unidades_de_Sangre = F("bloodUnitsCollected"),
                )
            )
            listCampaigns = list(listBloodDonationCampaign)

            if len(listCampaigns) > 0:
                campaign = listCampaigns[0]
                print(campaign)
                campaign['nombreEstado'] = dict(BloodDonationCampaignState.choices).get(campaign['Estado'])
                data={'message': "SUCCESS", "Campaigns" : campaign }
            else:
                data={'message':'Campaign Receiver not found...', 'Campaigns': []}
            return JsonResponse(data)

        else:
            listBloodDonationCampaign=list(BloodDonationCampaign.objects.select_related().values(
                    Id= F("id"),
                    Fecha= F("_date"),
                    Lugar= F("place"),
                    Estado= F("state"),
                    Observaciones = F("observations"),
                    Unidades_de_Sangre = F("bloodUnitsCollected"),
                )
            )
            if len(listBloodDonationCampaign)>0:
                data={"Campaigns":listBloodDonationCampaign}
            else:
                data={'message':'"Campaign Receiver not found...', 'Campaigns':[]}
        return JsonResponse(data)
    


    def post(self, request):
        jd = json.loads(request.body)
        tz = pytz.timezone('America/Guatemala')
        # Convertir la cadena ISO 8601 a un objeto datetime con información de zona horaria
        start_date = datetime.fromisoformat(jd['starDate'])
        # Configurar la zona horaria del objeto datetime
        start_date = tz.localize(start_date)
        print(start_date)
        bloodCampaign = BloodDonationCampaign.objects.create(
            _date=jd['_date'],
            starDate=start_date,
            place=jd['place'],
            state=jd['state'],
            observations=jd['observations'],
            bloodUnitsCollected=jd['bloodUnitsCollected']
        )
        print("Hora aquí")
        print(bloodCampaign.starDate)
        data = {'message': 'SUCCESS', 'id': bloodCampaign.id}
        return JsonResponse(data)
    
        #PUT
    def put(self,request,id):
        jd= json.loads(request.body)
        tz = pytz.timezone('America/Guatemala')
        start_date_str = jd['starDate']
        start_date = datetime.fromisoformat(start_date_str)
        start_date = tz.localize(start_date)
        print(start_date)

        listcampañas= list(BloodDonationCampaign.objects.filter(id=id).values()) #uno en especifico
        if len(listcampañas)>0:
            #con get lanza error sino aparece un el empleado, pero como ya esta anterior validado no importa
            lcampaña = BloodDonationCampaign.objects.get(id=id)
            #asiganmos valor a cada uno
            lcampaña.starDate=start_date
            lcampaña._date = jd['_date']
            lcampaña.place = jd['place']
            lcampaña.state = jd['state']    
            lcampaña.observations = jd['observations']                                
            lcampaña.bloodUnitsCollected = jd['bloodUnitsCollected']                                
            lcampaña.save() #se guardan los cambios
            datos = {"message": "Blood Campaign successfully edited"}
        else:
            datos={"message": "Blood Campaign , Blood Campaign not found to edit"}
        return JsonResponse(datos)
        
    #DELETE
    def delete (self, request,id):
        listcampañas = list(BloodDonationCampaign.objects.filter(id=id).values())
        if len(listcampañas)>0: #si existe tipo de usuario
            BloodDonationCampaign.objects.filter(id=id).delete()    
            datos = {"message": "Deleted, Blood Campaign  was successfully deleted"}
        else: #no existe
            datos={"message": "ERROR, Blood the Campaign  to delete was not found"}
        return JsonResponse(datos)
    
        
class UpdateStateCampaignView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
        #PUT
    def put(self,request,id):
        jd= json.loads(request.body)
        listcampañas= list(BloodDonationCampaign.objects.filter(id=id).values()) #uno en especifico
        if len(listcampañas)>0:
            #con get lanza error sino aparece un el empleado, pero como ya esta anterior validado no importa
            lcampaña = BloodDonationCampaign.objects.get(id=id)
            #asiganmos valor a cada uno
            lcampaña.state = jd['state']    
            lcampaña.save() #se guardan los cambios
            datos = {"message": "Blood Campaign state successfully edited"}
        else:
            datos={"message": "Blood Campaign , Blood Campaign not found to edit"}
        return JsonResponse(datos)
    
class CampaignsReportsView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get(self,req,id=0):
        if(id==0):
            listCampaigns=list(BloodDonationCampaign.objects.select_related().values(
                    "_date",
                    "starDate",
                    Id= F("id"),
                    Lugar= F("place"),
                    Estado= F("state"),
                    Observaciones = F("observations"),
                    Unidades_de_Sangre = F("bloodUnitsCollected"),
                )
            )
            if len(listCampaigns) > 0:
                for campaign in listCampaigns:
                    ListDonorsByBloodDonationCampaign=len(list((Donation.objects.select_related().filter(idBloodDonationCampaign=campaign['Id']).values('id'))))
                    campaign["TotalDonors"]=ListDonorsByBloodDonationCampaign
                    campaign['estado'] = dict(BloodDonationCampaignState.choices).get(campaign['Estado'])
                    if campaign['starDate'] != None:
                        campaign['Inicio']= campaign["starDate"].astimezone(pytz.timezone('America/New_York')).strftime("%d-%m-%Y")
                    else:
                        campaign['Inicio']=""
                    campaign['Fin']=campaign["_date"].strftime("%d-%m-%Y")
                data={'message': "SUCCESS", "Campaigns" : listCampaigns }
            else:
                data={'message':'Campaign Receiver not found...', 'Campaigns': []}
            return JsonResponse(data)
        #CAmpaña específica
        else:
            print(id)
            campaign=list(BloodDonationCampaign.objects.select_related().filter(id=id).values(
                    "id"
                ))
            if len(campaign)>0:
                donations = list(
                    Donation.objects.select_related()
                    .filter(idBloodDonationCampaign=id)
                    .values(
                        'id', 'bloodCorrelative', 'idBloodDonationCampaign','idDonationType','created_at','state', 'state',
                        Nombres=F('idDonor__idPerson__firstName'),
                        Apellidos=F('idDonor__idPerson__lastName'),
                        Grupo=F("idDonor__idBloodType__bloodType"),
                        Género=F("idDonor__idPerson__gender"),
                        Donación=F("idDonationType__donationType")
                    )
                )
                for i in donations:
                    i["Nombre"]=i["Nombres"]+" "+i["Apellidos"]
                    i["Fecha"]=i["created_at"].astimezone(pytz.timezone('America/New_York')).strftime("%d-%m-%Y")
                    i["Anotaciones"]=dict(DonationState.choices).get(i["state"])
                data={"Campaigns":donations}
                print(data)
            else:
                data={'message':'"Campaign Receiver not found...', 'Campaigns':[]}
        return JsonResponse(data)
            

