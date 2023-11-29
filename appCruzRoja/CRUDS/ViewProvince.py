from django.http.response import JsonResponse
from django.views import View
from ..models import *
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt 
import json

class ProvinceView(View):
    @method_decorator(csrf_exempt) #Saltamos restriccion
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self,req,id=0):
        id=int(id)
        if(id>0):
            provinces=list(Province.objects.filter(id=id).values())
            if len(provinces)>0:
                province=provinces[0]
                data={'message':"SUCCESS", 'Province':province}
            else:
                data={'message':"ERROR, provinces not found..."}
            return JsonResponse(data)
        else:
            provinces=list(Province.objects.values())
            if len(provinces)>0:
                data={'message':"SUCCESS", 'Provinces':provinces}
            else:
                data={'message':"ERROR, provinces not found..."}
            return JsonResponse(data)
    
    def post(self, req):
        jd=json.loads(req.body)
        Province.objects.create(province=jd['province'])
        data={'message':"SUCCESS"}
        return JsonResponse(data)
    
    def delete(self, req, id):
        provinces=list(Province.objects.filter(id=id).values())
        if provinces>0:
            Province.objects.filter(id=id).delete
            data={'message':"Province deleted"}
        else:
            data={'message':"ERROR, province not found"}
        return JsonResponse(data)
    
class SearchByProvinceId(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(req,self,idProvince):
        if idProvince>0:
            cities = City.objects.filter(idProvince_id=idProvince).values()
            if len(cities)>0:
                data={'message':"SUCCESS", "Cities":list(cities)}
            else:
                data={'message':"ERROR, cities not found...", "Cities":[]}
        return JsonResponse(data)  