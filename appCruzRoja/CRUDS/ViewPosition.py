from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from ..models import *
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt 
import json

# CRUD DE PROVINCE(Departamento)
class PositionView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self, request, id=0):
        if(id>0):
            positions=list(Position.objects.filter(id=id).values())
            if len(positions) > 0:
                position = positions[0]
                data={'message': "SUCCESS", "Position" : position}
            else:
                data={'message':'Position type not found...',"Position" : []}
        else:
            positions=list(Position.objects.values())
            if len(positions)>0:
                data={"Positions":positions}
            else:
                data={'message':'"Positions not found...', "Position" : []}
        return JsonResponse(data)
    
    def post(self, request):
        jd = json.loads(request.body)
        #print(jd)
        Position.objects.create(position=jd['position'])
        data={'message':'SUCCESS'}
        return JsonResponse(data)
        
