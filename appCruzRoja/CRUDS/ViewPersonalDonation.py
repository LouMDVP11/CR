from django.http.response import JsonResponse
from django.views import View
from ..models import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import FileSystemStorage
import base64
from django.db.models import F

from django.core import serializers


class PersonalDonationView(View):
    @method_decorator(csrf_exempt)  # Saltamos restriccion
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, req, id=0):
        id = int(id)
        if id > 0:
            personalDonations = list(PersonalDonation.objects.filter(id=id).values(
                "id", "_date", "_date", "_image","description", "idDonor_id", "idDonor_id__idPerson_id__firstName", "idDonor_id__idPerson_id__lastName" 
            ))
            if len(personalDonations) > 0:
                personalDonation = personalDonations[0]
                data = {"message": "SUCCESS", "PersonalDonation": personalDonation}
            else:
                data = {
                    "message": "ERROR, personalDonations not found...",
                    "PersonalDonation": [],
                }
            return JsonResponse(data)
        else:
            personalDonations = list(PersonalDonation.objects.values(
                    Id=F("id"),
                    Fecha=F("_date"),
                    Imagen=F("_image"),
                    Descripcion=F("description"),
                    Estado=F("state"),
                    IdDonor=F("idDonor_id"),
                    Nombre=F("idDonor_id__idPerson_id__firstName"),
                    Apellido=F("idDonor_id__idPerson_id__lastName"),
                )
            )
            if len(personalDonations) > 0:
                data = {"message": "SUCCESS", "PersonalDonation": personalDonations}
            else:
                data = {
                    "message": "ERROR, personalDonations not found...",
                    "PersonalDonation": [],
                }
            return JsonResponse(data)

    def post(self, req):
        jd = json.loads(req.body)
        uploaded_image = json.loads(jd["image"])
        if uploaded_image:
            uploaded_image = SimpleUploadedFile(
                name=uploaded_image["path"],
                content=base64.b64decode(uploaded_image["image"]),
            )
            fs = FileSystemStorage()
            filename = fs.save(
                uploaded_image.name, uploaded_image
            )  # Save the uploaded file
            destination_path = fs.url(filename)

            PersonalDonation.objects.create(
                _date=jd["date"],
                _image=destination_path,
                description=jd["description"],
                state=jd["state"],
                idDonor_id=jd["idDonor"],
            )
        else:
            PersonalDonation.objects.create(
                _date=jd["date"],
                _image=jd["image"],
                description=jd["description"],
                state=jd["state"],
                idDonor_id=jd["idDonor"],
            )
        data = {"message": "SUCCESS"}
        return JsonResponse(data)

    def put(self, req, id):
        jd = json.loads(req.body)
        if "image" in jd:
            uploaded_image = json.loads(jd["image"])
            if uploaded_image:
                uploaded_image = SimpleUploadedFile(
                    name=uploaded_image["path"],
                    content=base64.b64decode(uploaded_image["image"]),
                )
                fs = FileSystemStorage()
                filename = fs.save(
                    uploaded_image.name, uploaded_image
                )  # Save the uploaded file
                destination_path = fs.url(filename)

                personalDonation = PersonalDonation.objects.get(id=id)
                personalDonation._date = jd["date"]
                personalDonation._image = destination_path
                personalDonation.description = jd["description"]
                personalDonation.idDonor_id = jd["idDonor"]
               
                personalDonation.save()
                donor = Donor.objects.get(id=personalDonation.idDonor_id)
                person = Person.objects.get(id=donor.idPerson_id)
                personal_donation_data = {
                    "id": personalDonation.id,
                    "_date": personalDonation._date,
                    "_image": personalDonation._image,
                    "description": personalDonation.description,
                    "idDonor_id": donor.id,
                    "idDonor_id__idPerson_id__firstName" :person.firstName,
                    "idDonor_id__idPerson_id__lastName" :person.lastName,}
                data = {
                    "message": "SUCCESS",
                    "personalDonation": personal_donation_data,
                }
                return JsonResponse(data)
        else:
            personalDonation = PersonalDonation.objects.get(id=id)
            personalDonation._date = jd["date"]
            personalDonation.description = jd["description"]
            personalDonation.idDonor_id = jd["idDonor"]

            personalDonation.save()
            donor = Donor.objects.get(id=personalDonation.idDonor_id)
            person = Person.objects.get(id=donor.idPerson_id)
            personal_donation_data = {
                "id": personalDonation.id,
                "_date": personalDonation._date,
                "_image": personalDonation._image,
                "description": personalDonation.description,
                "idDonor_id": donor.id,
                "idDonor_id__idPerson_id__firstName" :person.firstName,
                "idDonor_id__idPerson_id__lastName" :person.lastName,}


            data = {"message": "SUCCESS", "personalDonation": personal_donation_data}

            return JsonResponse(data)


class PersonalDonationIDView(View):
    @method_decorator(csrf_exempt)  # Saltamos restriccion
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, req, id=0):
        id = int(id)
        if id > 0:
            personalDonations = list(
                PersonalDonation.objects.filter(idDonor_id=id).values(
                    Id=F("id"),
                    Fecha=F("_date"),
                    Imagen=F("_image"),
                    Descripcion=F("description"),
                    Estado=F("state"),
                    IdDonor=F("idDonor_id"),
                    Nombre=F("idDonor_id__idPerson_id__firstName"),
                    Apellido=F("idDonor_id__idPerson_id__lastName"),
                )
            )
            if len(personalDonations) > 0:
                personalDonation = personalDonations
                data = {"message": "SUCCESS", "PersonalDonation": personalDonation}
            else:
                data = {
                    "message": "ERROR, personalDonations not found...",
                    "PersonalDonation": [],
                }
            return JsonResponse(data)
        else:
            data = {
                "message": "ERROR, personalDonations not found...",
                "PersonalDonation": [],
            }
            return JsonResponse(data)

class UpdateSataetePersonaDonationView(View):  
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
      
    def put(self,req,id):
        jd=json.loads(req.body)
        existe = list(PersonalDonation.objects.filter(id=id).values())
        if len(existe)>0:
            personalEdit = PersonalDonation.objects.get(id=id)
            personalEdit.state=jd['state']
            personalEdit.save()
            datos = {"message": "SUCESS"}
        else:
            datos={"message": "ERROR"}
        return JsonResponse(datos)