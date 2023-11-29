from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt 
import json
from ..models import *



#------------------------------------------------ CRUD Donation Log ---------------------------------------------------------
class DonorAchievmentView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self, request, id=0):
        if(id>0):
            DonorAchievements=list(DonorAchievement.objects.filter(idDonor=id).select_related('idAchievement').values(
                'id','aquisitionDate','idAchievement','idDonor',
                'idAchievement__id','idAchievement__name','idAchievement__description','idAchievement__icon'
            ))
            if len(DonorAchievements) > 0:
                data={'message': "SUCCESS", "DonorAchievement" : DonorAchievements}
            else:
                data={'message':'ERROR DonorAchievement not found...', "DonorAchievement":[]}
        else:
                data={'message':'ERROR DonorAchievement not found...', "DonorAchievement":[]}
        return JsonResponse(data)
    
    def post(self, request):
        jd = json.loads(request.body)
        DonorAchievement.objects.create(aquisitionDate=jd['aquisitionDate'], idAchievement=jd['idAchievement'], idDonor=jd['idDonor'])
        data={'message':'SUCCESS'}
        return JsonResponse(data)
    
        #PUT
    def put(self,request,id):
        jd= json.loads(request.body)
        listDonorAchievements= list(DonorAchievement.objects.filter(id=id).values()) #uno en especifico
        if len(listDonorAchievements)>0:
            #con get lanza error sino aparece un el empleado, pero como ya esta anterior validado no importa
            lDonorAchievement = DonorAchievement.objects.get(id=id)
            #asiganmos valor a cada uno
            lDonorAchievement.aquisitionDate = jd['aquisitionDate']
            lDonorAchievement.idAchievement = jd['idAchievement']
            lDonorAchievement.idDonor = jd['idDonor']
            lDonorAchievement.save() #se guardan los cambios
            datos = {"message": "DonorAchievement successfully edited"}
        else:
            datos={"message": "DonorAchievement, DonorAchievement not found to edit"}
        return JsonResponse(datos)
        
    #DELETE
    def delete (self, request,id):
        listDonorAchievements = list(DonorAchievement.objects.filter(id=id).values())
        if len(listDonorAchievements)>0: #si existe tipo de usuario
            DonorAchievement.objects.filter(id=id).delete()    
            datos = {"message": "Deleted, the Donor Achievment was successfully deleted"}
        else: #no existe
            datos={"message": "ERROR, the Donor Achievment to delete was not found"}
        return JsonResponse(datos)
    
        
