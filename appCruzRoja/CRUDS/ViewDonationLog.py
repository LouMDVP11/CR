from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt 
import json
from ..models import *

#------------------------------------------------ CRUD Donation Log ---------------------------------------------------------
class DonationlogV(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self, request, id=0):
        if(id>0):
            donationlogs=list(DonationLog.objects.filter(id=id).values())
            if len(donationlogs) > 0:
                donationlog = donationlogs[0]
                data={'message': "SUCCESS", "Donation Log" : donationlog}
            else:
                data={'message':'Donation Log not found...'}
        else:
            donationlogs=list(DonationLog.objects.values())
            if len(donationlogs)>0:
                data={"Donation Log":donationlogs}
            else:
                data={'message':'"Donation log not found...'}
        return JsonResponse(data)
    
    def post(self, request):
        jd = json.loads(request.body)
        DonationLog.objects.create(description=jd['description'], idDonation=jd['idDonation'])
        data={'message':'SUCCESS'}
        return JsonResponse(data)
    
        #PUT
    def put(self,request,id):
        jd= json.loads(request.body)
        listdonationlogs= list(DonationLog.objects.filter(id=id).values()) #uno en especifico
        if len(listdonationlogs)>0:
            #con get lanza error sino aparece un el empleado, pero como ya esta anterior validado no importa
            ldonationlog = DonationLog.objects.get(id=id)
            #asiganmos valor a cada uno
            ldonationlog.description = jd['description']
            ldonationlog.idDonation = jd['idDonation']
            ldonationlog.save() #se guardan los cambios
            datos = {"message": "Donation Log successfully edited"}
        else:
            datos={"message": "Donation Type, Donation type not found to edit"}
        return JsonResponse(datos)
        
    #DELETE
    def delete (self, request,id):
        listdonationlogs = list(DonationLog.objects.filter(id=id).values())
        if len(listdonationlogs)>0: #si existe tipo de usuario
            DonationLog.objects.filter(id=id).delete()    
            datos = {"message": "Deleted, the Donation Log was successfully deleted"}
        else: #no existe
            datos={"message": "ERROR, the Donation Type to delete was not found"}
        return JsonResponse(datos)
    
        
