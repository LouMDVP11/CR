from typing import Any
from django import http
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from ..models import *
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt 
import json

class PublicationLogView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args,**kwargs)
    
    #------- Get Publication Log(s)
    def get(self, request, id=0):
        #-- If looking for an specific log
        if(id>0):
            listPublicationLogs = list(PublicationLog.objects.filter(id=id).values())
            if len(listPublicationLogs)>0:
                publicationLog=listPublicationLogs[0]
                datos= {'message': "SUCCESS", "Publication log" : publicationLog}
            else:
                datos={"message": "ERROR, publication log no found"}
            return JsonResponse(datos) 
        #-- If looking for every publication log
        else:
            listPublicationLogs = list(PublicationLog.objects.values()) 
            if len(listPublicationLogs)>0: 
                datos= {'message': "SUCCESS", "List of Publication Logs" : listPublicationLogs}
            else :
                datos={"message": "ERROR, list of publication logs not found"} 
            return JsonResponse(datos)
    
    #-------- Post a new publication Log
    def post(self, request):
        jd = json.loads(request.body)
        PublicationLog.objects.create(
            description=jd['description'],
            idPublication=jd['idPublication'],
        )    
        datos={"message": "SUCCESS, publication created"}
        return JsonResponse(datos)
    
    #-------- Put on table publication log (edit)
    def put(self,request,id):
        jd= json.loads(request.body)
        listPublicationLogs= list(PublicationLog.objects.filter(id=id).values()) 
        # If exists a publication log with the id received
        if len(listPublicationLogs)>0:
            publicationLog = PublicationLog.objects.get(id=id)
            publicationLog.description=jd['description'],
            publicationLog.idPublication=jd['idPublication'],
            
            publicationLog.save() #se guardan los cambios
            datos = {"message": "Publication log update successful"}
        else:
            datos={"message": "Error, publication log not found"}
        return JsonResponse(datos)

    #--------- Delete a publication Log
    def delete (self, request,id):
        listPublicationLogs = list(PublicationLog.objects.filter(id=id).values())
        # If exist the publication log with the id received
        if len(listPublicationLogs)>0: 
            PublicationLog.objects.filter(id=id).delete()    
            datos = {"message": "DELETE, publication log deleted"}
        # If doesn't exist
        else:
            datos={"message": "ERROR, not found publication log"}
        return JsonResponse(datos)
        