from typing import Any
from django import http
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from ..models import *
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt 
import json

class DonorSuspendedLogView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args,**kwargs)
    
    #------- Get Motive Log(s)
    def get(self, request, id=0):
        #-- If looking for an specific donor suspended Log
        if(id>0):
            listDonorSuspendedLogs = list(DonorSuspendedLog.objects.filter(id=id).values())
            if len(listDonorSuspendedLogs)>0:
                donorSuspendedLog=listDonorSuspendedLogs[0]
                datos= {'message': "SUCCESS", "Donor suspended log" : donorSuspendedLog}
            else:
                datos={"message": "ERROR, donor suspended log not found"}
            return JsonResponse(datos) 
        #-- If looking for every donor suspended log
        else:
            listDonorSuspendedLogs = list(DonorSuspendedLog.objects.values()) 
            if len(listDonorSuspendedLogs)>0: 
                datos= {'message': "SUCCESS", "List of donor suspended logs" : listDonorSuspendedLogs}
            else :
                datos={"message": "ERROR, list of donor suspended logs not found"} 
            return JsonResponse(datos)
    
    #-------- Post a new donor suspended log
    def post(self, request):
        jd = json.loads(request.body)
        Motive.objests.create(
            initialDate=jd['initialDate'],
            finalDate=jd['finalDate'],
            idDonor=jd['idDonor'],
            idMotive=jd['idMotive'],
        )    
        datos={"message": "SUCCESS, donor suspended log created"}
        return JsonResponse(datos)
    
    #-------- Put on table Donor suspended log (edit)
    def put(self,request,id):
        jd= json.loads(request.body)
        listDonorSuspendedLogs= list(DonorSuspendedLog.objects.filter(id=id).values()) 
        # If exist the publication log with the id received
        if len(listDonorSuspendedLogs)>0:
            donorSuspendedLog = DonorSuspendedLog.objects.get(id=id)
            donorSuspendedLog.initialDate=jd['initialDate'],
            donorSuspendedLog.finalDate=jd['finalDate'],
            donorSuspendedLog.idDonor=jd['idDonor'],
            donorSuspendedLog.idMotive=jd['idMotive'],
            
            donorSuspendedLog.save() #se guardan los cambios
            datos = {"message": "Donor suspended log update successful"}
        else:
            datos={"message": "Error, donor suspended log doesn't exist"}
        return JsonResponse(datos)

    #--------- Delete a donor suspended Log
    def delete (self, request,id):
        listDonorSuspendedLogs = list(DonorSuspendedLog.objects.filter(id=id).values())
        # If exists a donor suspended log with the id received
        if len(listDonorSuspendedLogs)>0: 
            DonorSuspendedLog.objects.filter(id=id).delete()    
            datos = {"message": "DELETE, donor suspended log deleted"}
        # If doesn't exist
        else:
            datos={"message": "ERROR, not found donor suspended log"}
        return JsonResponse(datos)
        