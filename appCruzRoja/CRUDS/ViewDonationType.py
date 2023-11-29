from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt 
import json
from ..models import *


#------------------------------------------------ CRUD Donation Type ---------------------------------------------------------
class DonationTypeView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self, request, id=0):
        if(id>0):
            donationtypes=list(DonationType.objects.filter(id=id).values())
            if len(donationtypes) > 0:
                donationtype = donationtypes[0]
                data={'message': "SUCCESS", "DonationType" : donationtype}
            else:
                data={'message':'Donation type not found...','DonationType':[]}
        else:
            donationtypes=list(DonationType.objects.values())
            if len(donationtypes)>0:
                data={"DonationType":donationtypes}
            else:
                data={'message':'"Donation types not found...', 'DonationType':[]}
        return JsonResponse(data)
    
    def post(self, request):
        jd = json.loads(request.body)

        DonationType.objects.create(donationtype=jd['donationtype'])
        data={'message':'SUCCESS'}
        return JsonResponse(data)
    
        #PUT
    def put(self,request,id):
        jd= json.loads(request.body)
        listDonationTypes= list(DonationType.objects.filter(id=id).values()) #uno en especifico
        if len(listDonationTypes)>0:
            #con get lanza error sino aparece un el empleado, pero como ya esta anterior validado no importa
            lDonationType = DonationType.objects.get(id=id)
            #asiganmos valor a cada uno
            lDonationType.donationType = jd['donationType']
            lDonationType.save() #se guardan los cambios
            datos = {"message": "DonationType successfully edited"}
        else:
            datos={"message": "Donation Type, Donation type not found to edit"}
        return JsonResponse(datos)
        
    #DELETE
    def delete (self, request,id):
        listDonationTypes = list(DonationType.objects.filter(id=id).values())
        if len(listDonationTypes)>0: #si existe tipo de usuario
            DonationType.objects.filter(id=id).delete()    
            datos = {"message": "Deleted, the DonationType was successfully deleted"}
        else: #no existe
            datos={"message": "ERROR, the Donation Type to delete was not found"}
        return JsonResponse(datos)
    
        
