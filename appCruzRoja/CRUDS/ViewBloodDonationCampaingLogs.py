from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from ..models import *
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt 
import json

#------------------------------------------------ CRUD Campaign---------------------------------------------------------
class BoodDonationCampingLogView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self, request, id=0):
        if(id>0):
            listBloodDonationCamigLogs=list(BloodDonationCampaingLog.objects.filter(id=id).values())
            if len(listBloodDonationCamigLogs) > 0:
                bloodDonationCamLog = listBloodDonationCamigLogs[0]
                data={'message': "SUCCESS", "Blood Donation Campaign Log" : bloodDonationCamLog}
            else:
                data={'message':'Blood Donation Campaign Log not found...'}
            return JsonResponse(data) 

        else:
            listBloodDonationCamigLogs=list(BloodDonationCampaingLog.objects.values())
            if len(listBloodDonationCamigLogs)>0:
                data={"List of Blood Donation Campaign Log":listBloodDonationCamigLogs}
            else:
                data={'message':'List of Blood Donation Campaign Log not found...'}
            return JsonResponse(data)
    
    def post(self, request):
        jd = json.loads(request.body)
        BloodDonationCampaingLog.objects.create(
            description=jd['description'],
            idBloodDonationCampaign=jd['idBloodDonationCampaign'],
            )
        data={'message':'SUCCESS, bloodDonationCamLog receiver created'}
        return JsonResponse(data)
    
        #PUT
    def put(self,request,id):
        jd= json.loads(request.body)
        bloodDonationCampLog= list(BloodDonationCampaingLog.objects.filter(id=id).values()) #uno en especifico
        if len(bloodDonationCampLog)>0:
            bloodDonationCampLog = BloodDonationCampaingLog.objects.get(id=id)
            bloodDonationCampLog.description = jd['description']
            bloodDonationCampLog.idBloodDonationCampaign = jd['idBloodDonationCampaign']
            bloodDonationCampLog.save() 
            data = {"message": "bloodDonationCamLog successfully edited"}
        else:
            data={"message": "Error, bloodDonationCamLog not found to edit"}
        return JsonResponse(data)
        
    #DELETE
    def delete (self, request,id):
        bloodDonationCampLog = list(BloodDonationCampaingLog.objects.filter(id=id).values())
        if len(bloodDonationCampLog)>0: #si existe tipo de usuario
            BloodDonationCampaingLog.objects.filter(id=id).delete()    
            data = {"message": "Deleted,Blood Donation campaign Log was successfully deleted"}
        else: #no existe
            data={"message": "ERROR, the blood donation campaign log to delete was not found"}
        return JsonResponse(data)
    
        
