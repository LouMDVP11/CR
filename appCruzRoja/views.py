from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .models import *
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt 
import json

# CRUD DE PROVINCE(Departamento)
class ProvinceView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self, request, id=0):
        if(id>0):
            deps=list(Province.objects.filter(id=id).values())
            if len(deps) > 0:
                dep = deps[0]
                datos={'message': "CORRECTO", "Departamento" : dep}
            else:
                datos={'message':'Departamento not found...'}
        else:
            deps=list(Province.objects.values())
            if len(deps)>0:
                datos={"Departamentos":deps}
            else:
                datos={'message':'"Departamentos no encontrado...'}
        return JsonResponse(datos)
    
    def post(self, request):
        jd = json.loads(request.body)
        #print(jd)
        Province.objects.create(province=jd['province'])
        datos={'message':'Success'}
        return JsonResponse(datos)
        
