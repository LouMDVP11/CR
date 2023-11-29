from django.http.response import JsonResponse
from django.views import View
from ..models import *
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt 
import json

class CityView(View):
    @method_decorator(csrf_exempt) #Saltamos restriccion
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self,req,id=0):
        id=int(id)
        if(id>0):
            cities=list(City.objects.filter(id=id).values())
            if len(cities)>0:
                city=cities[0]
                data={'message':"SUCCESS", 'City':city}
            else:
                data={'message':"ERROR, cities not found..."}
            return JsonResponse(data)
        else:
            cities=list(City.objects.values())
            if len(cities)>0:
                data={'message':"SUCCESS", 'Cities':cities}
            else:
                data={'message':"ERROR, cities not found..."}
            return JsonResponse(data)
    
    def post(self, req):
        jd=json.loads(req.body)
        province = Province.objects.get(id=jd['id_province'])
        City.objects.create(city=jd['city'], idProvince=province)
        data={'message':"SUCCESS"}
        return JsonResponse(data)
    
    def delete(self, req, id):
        cities=list(City.objects.filter(id=id).values())
        if cities>0:
            City.objects.filter(id=id).delete
            data={'message':"City deleted"}
        else:
            data={'message':"ERROR, city not found"}
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
    
