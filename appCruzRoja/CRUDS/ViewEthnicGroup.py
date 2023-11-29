from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from ..models import *
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt 
import json

#------------------------------------------------ CRUD DE EthnicGroup ---------------------------------------------------------
class EthnicGroupView(View):
    @method_decorator(csrf_exempt) 
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    #GET
    def get(self,request,id=0): 
        if(id>0): 
            listEthnicGroups= list(EthnicGroup.objects.filter(id=id).values()) 
            if len(listEthnicGroups)>0:
                ethnic=listEthnicGroups[0]
                datos= {'message': "SUCCESS", "EthincGroup" : ethnic}
            else:
                datos={"message": "ERROR, EthnicGroup no found"}
            return JsonResponse(datos) 
                
        else: 
            listEthnicGroups = list(EthnicGroup.objects.values()) 
            if len(listEthnicGroups)>0: 
                datos= {'message': "SUCCESS", "EthnicGroups" : listEthnicGroups}
            else :
                datos={"message": "ERROR,EthnicGroups not found"} 
            return JsonResponse(datos)

    #POST
    def post(self, request):
        jd= json.loads(request.body)
        EthnicGroup.objects.create(ethnicGroup=jd['ethnicGroup'])
        print (jd) 
        datos={"message": "SUCCESS, EthicGroup created"}
        return JsonResponse(datos)
          
    #PUT
    def put(self,request,id):
        jd= json.loads(request.body)
        listEthnicGroups= list(EthnicGroup.objects.filter(id=id).values()) 
        if len(listEthnicGroups)>0:
            ethnic = EthnicGroup.objects.get(id=id)
            ethnic.ethnicGroup= jd['ethnicGroup']
            ethnic.save() 
            datos = {"message": "Ethnic group update successful"}
        else:
            datos={"message": "Error, Ethnic group update"}
        return JsonResponse(datos)
        
    #DELETE
    def delete (self, request,id):
        listEthnicGroups = list(EthnicGroup.objects.filter(id=id).values())
        if len(listEthnicGroups)>0: 
            EthnicGroup.objects.filter(id=id).delete()    
            datos = {"message": "DELETE, ethnicGroup deleted"}
        else: #no existe
            datos={"message": "ERROR,  ethnic not found"}
        return JsonResponse(datos)
        
