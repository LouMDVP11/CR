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
from django.core.mail import send_mail

class PublicationView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args,**kwargs)
    
    #------- Get Publication
    def get(self, request, id=0):
        #-- If looking for an specific publication
        if(id>0):
            listPublications = list(Publication.objects.filter(id=id).values())
            if len(listPublications)>0:
                publication=listPublications[0]
                datos= {'message': "SUCCESS", "Publication" : publication}
            else:
                datos={"message": "ERROR, publication no found"}
            return JsonResponse(datos) 
        #-- If looking for every publication
        else:
            listPublications = list(Publication.objects.values().order_by('-id')) 
            if len(listPublications)>0: 
                datos= {'message': "SUCCESS", "List of Publications" : listPublications}
            else :
                datos={"message": "ERROR, list of publications not found", "List of Publications" : []} 
            return JsonResponse(datos)
    
    #-------- Post a new publication
    def post(self, request):
        jd = json.loads(request.body.decode('utf-8'))
        uploaded_image = json.loads(jd['multimedia'])
        employee = Employee.objects.get(id=jd['idEmployee'])
        if uploaded_image:
            uploaded_image = SimpleUploadedFile(
                name=uploaded_image['path'],
                content=base64.b64decode(uploaded_image['image'])
            )

            fs = FileSystemStorage()
            filename = fs.save(uploaded_image.name, uploaded_image)  # Save the uploaded file
            destination_path = fs.url(filename)

            print(jd['_priority'])
            Publication.objects.create(
                title=jd['title'], 
                _priority=jd['_priority'],
                expirationDate=jd['expirationDate'],
                _content=jd['_content'], 
                multimedia=destination_path,
                idEmployee=employee
            )
            datos = {"message": "SUCCESS, publication created"}
        else:
            Publication.objects.create(
                title=jd['title'], 
                _priority=jd['_priority'],
                expirationDate=jd['expirationDate'],
                _content=jd['_content'], 
                multimedia=jd['multimedia'],
                idEmployee=employee
            )
            datos = {"message": "SUCCESS, publication created"}
        subject = 'Nueva publicación de Cruz Roja'
        message = jd['title'] + '\n\n' + jd['_content'] + "\nPara ver más detalles, ingresa a la página de Cruz Roja para visualizar la publicación. Enlace a la página: http://localhost:3000/publications"
        from_email = 'cruzrojaxela@outlook.com'
        recipient_list = ['cruzrojaxela@outlook.com']
        listPeople  = Person.objects.values()
        print(listPeople)
        for row in listPeople:
            print(row)
            recipient_list.append(row['email'])
        try:
            send_mail(subject, message, from_email, recipient_list)
            return JsonResponse(datos)
        except Exception as e:
            print('Error al enviar el correo.') 
            return JsonResponse(datos)
    
    #-------- Put on table publication (edit)
    def put(self,request,id):
        jd= json.loads(request.body)
        listPublications= list(Publication.objects.filter(id=id).values()) 
        if len(listPublications)>0:
            publication = Publication.objects.get(id=id)
            publication._priority=jd['_priority'],
            publication.title=jd['title'],
            publication._content=jd['_content'],
            publication.expirationDate=jd['expirationDate'],
            publication.multimedia=jd['multimedia'],
            publication.idEmployee=jd['idEmployee'],
            
            publication.save() #se guardan los cambios
            datos = {"message": "Publication update successful"}
        else:
            datos={"message": "Error, publication not found"}
        return JsonResponse(datos)

    #--------- Delete a publication
    def delete (self, request,id):
        listPublications = list(Publication.objects.filter(id=id).values())
        # If exists a publication with the id received
        if len(listPublications)>0: 
            Publication.objects.filter(id=id).delete()    
            datos = {"message": "DELETE, publication deleted"}
        # If doesn't exist
        else:
            datos={"message": "ERROR, not found publication"}
        return JsonResponse(datos)
        
 
class UpdatePublicationView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args,**kwargs)
    
    #-------- Put on table publication (edit)
    def post(self,request,id):
        jd= json.loads(request.body.decode('utf-8'))
        #print(jd['title'])
        uploaded_image = json.loads(jd['multimedia'])
        listPublications= list(Publication.objects.filter(id=id).values()) 
        if len(listPublications)>0:
            publication = Publication.objects.get(id=id)
            if uploaded_image:
                uploaded_image = SimpleUploadedFile(
                    name=uploaded_image['path'],
                    content=base64.b64decode(uploaded_image['image'])
                )

                fs = FileSystemStorage()
                filename = fs.save(uploaded_image.name, uploaded_image)  # Save the uploaded file
                destination_path = fs.url(filename)
                publication.multimedia=destination_path
            else:
                publication.multimedia=jd['multimedia']
            publication._priority=jd['_priority']
            publication.title=jd['title']
            publication._content=jd['_content']
            publication.expirationDate=jd['expirationDate']
            
            publication.save() #se guardan los cambios
            datos = {"message": "Publication update successful"}
        else:
            datos={"message": "Error, publication not found"}
        return JsonResponse(datos)


class UpdatePublicationNPView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args,**kwargs)
    
    #-------- Put on table publication (edit)
    def post(self,request,id):
        jd= json.loads(request.body.decode('utf-8'))
        print(jd['title'])
        listPublications= list(Publication.objects.filter(id=id).values()) 
        if len(listPublications)>0:
            print("Hola")
            publication = Publication.objects.get(id=id)
            publication._priority=jd['_priority']
            publication.title=jd['title']
            publication._content=jd['_content']
            if(jd['expirationDate']==""):
                publication.expirationDate="null"
            else:
                publication.expirationDate=jd['expirationDate']
            
            
            publication.save() #se guardan los cambios
            datos = {"message": "Publication update successful"}
        else:
            datos={"message": "Error, publication not found"}
        return JsonResponse(datos)