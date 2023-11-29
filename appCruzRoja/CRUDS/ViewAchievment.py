from typing import Any
from django import http
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from ..models import *
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt 
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import FileSystemStorage
import json
import base64
from django.db.models import F

#------------------------------------------------ CRUD Donation Log ---------------------------------------------------------
class AchievmentV(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self, request, id=0):
        if(id>0):
            Achievments=list(Achievement.objects.filter(id=id).values(
                Nombre=F('name'),
                Descripción=F('description'),
                DonacionesRequeridas=F('amount'),
                Image=F('icon')
            ))
            if len(Achievments) > 0:
                achievment = Achievments[0]
                data={'message': "SUCCESS", "Achievment" : achievment}
            else:
                data={'message':'Achievment not found...',"Achievment" : []}
        else:
            Achievments=(Achievement.objects.values(
                'id',
                'amount',
                Nombre=F('name'),
                Descripción=F('description'),
                Image=F('icon')
            ))
            if len(Achievments)>0:
                for i in Achievments:
                    i['Donaciones requeridas']=i['amount']
                    del i['amount']
                data={"Achievment":list(Achievments)}
            else:
                data={'message':'"Achievment not found...',"Achievment":[]}
        return JsonResponse(data)
    
    def post(self, request):
        jd = json.loads(request.body.decode('utf-8'))
        uploaded_image = json.loads(jd['icon'])
        if uploaded_image:
            uploaded_image = SimpleUploadedFile(
                name=uploaded_image['path'],
                content=base64.b64decode(uploaded_image['image'])
            )

            fs = FileSystemStorage()
            filename = fs.save(uploaded_image.name, uploaded_image)  # Save the uploaded file
            destination_path = fs.url(filename)

            Achievement.objects.create(name=jd['name'], description=jd['description'], amount=jd['amount'],duration=None, icon=destination_path)
            datos = {"message": "SUCCESS"}
        else:
            datos = {"message": "ERROR, no file received"}

        return JsonResponse(datos)
    
        #PUT
    def put(self,request,id):
        jd= json.loads(request.body)
        listAchievments= list(Achievement.objects.filter(id=id).values()) #uno en especifico
        if len(listAchievments)>0:
            #con get lanza error sino aparece un el empleado, pero como ya esta anterior validado no importa
            lachievment = Achievement.objects.get(id=id)
            #asiganmos valor a cada uno
            lachievment.name = jd['name']
            lachievment.requirement = jd['requirement']
            lachievment.icon = jd['icon']            
            lachievment.save() #se guardan los cambios
            datos = {"message": "Achievment successfully edited"}
        else:
            datos={"message": "Achievment, Achievment not found to edit"}
        return JsonResponse(datos)
        
    #DELETE
    
    
class UpdateAchievement(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get (self, request,id):
        listAchievments = list(Achievement.objects.filter(id=id).values())
        if len(listAchievments)>0: #si existe tipo de usuario
            Achievement.objects.filter(id=id).delete()    
            datos = {"message": "Deleted, the Achievment was successfully deleted"}
        else: #no existe
            datos={"message": "ERROR, the Achievment to delete was not found"}
        return JsonResponse(datos)
    
    
    def post(self, request, id):
        jd = json.loads(request.body.decode('utf-8'))
        uploaded_image = json.loads(jd['icon'])
        listAchievments= list(Achievement.objects.filter(id=id).values()) #uno en especifico
        if uploaded_image:
            if len(listAchievments)>0:
                uploaded_image = SimpleUploadedFile(
                name=uploaded_image['path'],
                content=base64.b64decode(uploaded_image['image'])
                )

                fs = FileSystemStorage()
                filename = fs.save(uploaded_image.name, uploaded_image)  # Save the uploaded file
                destination_path = fs.url(filename)
                #con get lanza error sino aparece un el empleado, pero como ya esta anterior validado no importa
                lachievment = Achievement.objects.get(id=id)
                #asiganmos valor a cada uno
                lachievment.name = jd['name']
                lachievment.requirement = jd['requirement']
                lachievment.icon = destination_path        
                lachievment.save() #se guardan los cambios
                datos = {"message": "SUCCESS"}
            else:
                datos={"message": "ERROR, Achievment not found to edit"}
        else:
            datos = {"message": "ERROR, no file received"}

        return JsonResponse(datos)
