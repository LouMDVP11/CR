from typing import Any
from django import http
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from ..models import *
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt 
import json

class MotiveView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args,**kwargs)
    
    #------- Get Motive(s)
    def get(self, request, id=0):
        #-- If looking for an specific motive
        if(id>0):
            listMotives = list(Motive.objects.filter(id=id).values())
            if len(listMotives)>0:
                motive=listMotives[0]
                datos= {'message': "SUCCESS", "Motive" : motive}
            else:
                datos={"message": "ERROR, motive not found"}
            return JsonResponse(datos) 
        #-- If looking for every motive
        else:
            listMotives = list(Motive.objects.values()) 
            if len(listMotives)>0: 
                datos= {'message': "SUCCESS", "List of motives" : listMotives}
            else :
                datos={"message": "ERROR, list of motives not found"} 
            return JsonResponse(datos)
    
    #-------- Post a new Motive
    def post(self, request):
        jd = json.loads(request.body)
        Motive.objests.create(
            motive=jd['motive'],
            suspendedTime=jd['suspendedTime'],
        )    
        datos={"message": "SUCCESS, motive created"}
        return JsonResponse(datos)
    
    #-------- Put on table motive (edit)
    def put(self,request,id):
        jd= json.loads(request.body)
        listMotives= list(Motive.objects.filter(id=id).values()) 
        # If exist the publication log with the id received
        if len(listMotives)>0:
            motive = Motive.objects.get(id=id)
            motive.motive=jd['motive'],
            motive.suspendedTime=jd['suspendedTime'],
            
            motive.save() #se guardan los cambios
            datos = {"message": "Motive update successful"}
        else:
            datos={"message": "Error, motive doesn't exist"}
        return JsonResponse(datos)

    #--------- Delete a motive
    def delete (self, request,id):
        listMotives = list(Motive.objects.filter(id=id).values())
        # If exists a motive with the id received
        if len(listMotives)>0: 
            Motive.objects.filter(id=id).delete()    
            datos = {"message": "DELETE, motive deleted"}
        # If doesn't exist
        else:
            datos={"message": "ERROR, not found motive"}
        return JsonResponse(datos)
        