from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from ..models import *
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt 
import json

# CRUD DE PROVINCE(Departamento)
class BloodTypeView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self, request, id=0):
        if(id>0):
            bloodtypes=list(BloodType.objects.filter(id=id).values())
            if len(bloodtypes) > 0:
                bloodtype = bloodtypes[0]
                data={'message': "SUCCESS", "Blood type" : bloodtype}
            else:
                data={'message':'Blood type not found...'}
        else:
            bloodtypes=list(BloodType.objects.values())
            if len(bloodtypes)>0:
                data={"Blood types":bloodtypes}
            else:
                data={'message':'"Blood types not found...'}
        return JsonResponse(data)
    
    def post(self, request):
        jd = json.loads(request.body)
        #print(jd)
        BloodType.objects.create(bloodType=jd['bloodType'])
        data={'message':'SUCCESS'}
        return JsonResponse(data)
        
