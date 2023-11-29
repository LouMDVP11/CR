from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from ..models import *
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt 
import json

#------------------------------------------------ CRUD Campaign---------------------------------------------------------
class CampaignBloodTypeView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self, request, id=0):
        if(id>0):
            listCampaignBloodType=list(CampaignBloodType.objects.filter(id=id).values())
            if len(listCampaignBloodType) > 0:
                campaignBloodType1 = listCampaignBloodType[0]
                data={'message': "SUCCESS", "Campaign Blood Type" : campaignBloodType1}
            else:
                data={'message':'Campaign Blood Type not found...'}
            return JsonResponse(data) 

        else:
            listCampaignBloodType=list(CampaignBloodType.objects.values())
            if len(listCampaignBloodType)>0:
                data={"Campaign Blood Type":listCampaignBloodType}
            else:
                data={'message':'"Campaign Blood Type not found...'}
            return JsonResponse(data)
    
    def post(self, request):
        jd = json.loads(request.body)
        CampaignBloodType.objects.create(
            bloodUnitsReceived=jd['bloodUnitsReceived'],
            purpose=jd['purpose'],
            units=jd['units'],
            idReceiver=jd['idReceiver'],
            idBloodDonationCampaign=jd['idBloodDonationCampaign']            
            )
        data={'message':'SUCCESS, campaignBloodType1 receiver created'}
        return JsonResponse(data)
    
        #PUT
    def put(self,request,id):
        jd= json.loads(request.body)
        listCampaignReceivers= list(CampaignBloodType.objects.filter(id=id).values()) #uno en especifico
        if len(listCampaignReceivers)>0:
            campaignR = CampaignBloodType.objects.get(id=id)
            campaignR.idBloodType = jd['idBloodType']
            campaignR.idCampaignReceiver = jd['idCampaignReceiver']
            campaignR.save() 
            data = {"message": "Campaign Blood Type successfully edited"}
        else:
            data={"message": "Error, Campaign Blood Type not found to edit"}
        return JsonResponse(data)
        
    #DELETE
    def delete (self, request,id):
        listCampaignReceivers = list(CampaignBloodType.objects.filter(id=id).values())
        if len(listCampaignReceivers)>0: #si existe tipo de usuario
            CampaignBloodType.objects.filter(id=id).delete()    
            data = {"message": "Deleted, Campaign Blood Type was successfully deleted"}
        else: #no existe
            data={"message": "ERROR, the Campaign Blood Type to delete was not found"}
        return JsonResponse(data)
    
        
