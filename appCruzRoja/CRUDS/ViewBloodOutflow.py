from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt 
import json

#------------------------------------------------ CRUD Blood Out Flow---------------------------------------------------------
class BloodOutflow(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self, request, id=0):
        if(id>0):
            Bloods=list(BloodOutflow.objects.filter(id=id).values())
            if len(Bloods) > 0:
                Blood = Bloods[0]
                data={'message': "SUCCESS", "Blood Out Flow" : Blood}
            else:
                data={'message':'DBlood Out Flow not found...'}
        else:
            Bloods=list(BloodOutflow.objects.values())
            if len(Bloods)>0:
                data={"Blood types":Bloods}
            else:
                data={'message':'"Blood Out Flow not found...'}
        return JsonResponse(data)
    
    def post(self, request):
        jd = json.loads(request.body)

        BloodOutflow.objects.create(outflowDate=jd['outflowDate'], idDonation=jd['idDonation'])
        data={'message':'SUCCESS'}
        return JsonResponse(data)
    
        #PUT
    def put(self,request,id):
        jd= json.loads(request.body)
        listBloods= list(BloodOutflow.objects.filter(id=id).values()) #uno en especifico
        if len(listBloods)>0:
            #con get lanza error sino aparece un el empleado, pero como ya esta anterior validado no importa
            lBlood = BloodOutflow.objects.get(id=id)
            #asiganmos valor a cada uno
            lBlood.outflowDate = jd['outflowDate']
            lBlood.idDonation = jd['idDonation']
            lBlood.save() #se guardan los cambios
            datos = {"message": "Blood Out Flow successfully edited"}
        else:
            datos={"message": "Blood Out Flow, Blood Out Flow not found to edit"}
        return JsonResponse(datos)
        
    #DELETE
    def delete (self, request,id):
        listBloods = list(BloodOutflow.objects.filter(id=id).values())
        if len(listBloods)>0: #si existe tipo de usuario
            BloodOutflow.objects.filter(id=id).delete()    
            datos = {"message": "Deleted, the Blood Out Flow was successfully deleted"}
        else: #no existe
            datos={"message": "ERROR, the Blood Out Flow to delete was not found"}
        return JsonResponse(datos)
    
        
