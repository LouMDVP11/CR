from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from ..models import *
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import F
from django.db.models import Q

from datetime import datetime, timedelta

from django.core.mail import send_mail


# ------------------------------------------------ CRUD DE Donation ---------------------------------------------------------
class DonationView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # GET
    def get(self, request, id=0):
        if id > 0:
            donations = (
                Donation.objects.select_related(
                    "idDonationType", "idDonor", "idBloodDonationCampaign"
                )
                .filter(id=id)
                .values(
                    IdDonacion=F("id"),
                    Correlativo=F("correlative"),
                    Correlativo_Sangre=F("bloodCorrelative"),
                    idEstadoDonacion=F("state"),
                    Observaciones=F("comments"),
                    Peso=F("weight"),
                    Temperatura=F("temperature"),
                    Presion=F("bloodPressure"),
                    Hemoglobina=F("hemoglobin"),
                    IdJornada=F("idBloodDonationCampaign_id"),
                    LugarJornada=F("idBloodDonationCampaign__place"),
                    FechaJornada=F("idBloodDonationCampaign___date"),
                    IdTipoDonacion=F("idDonationType_id"),
                    TipoDonacion=F("idDonationType__donationType"),
                    IdDonor=F("idDonor_id"),
                    DPI=F("idDonor__idPerson__dpi"),
                    ID_Extranjero=F("idDonor__idPerson__idExtranjero"),
                    Nombre=F("idDonor__idPerson__firstName"),
                    Apellido=F("idDonor__idPerson__lastName"),
                    CorreoElectronico=F("idDonor__idPerson__email"),
                    idGenero=F("idDonor__idPerson__gender"),
                    FechaNacimiento=F("idDonor__idPerson__birthDate"),
                    DireccionCasa=F("idDonor__homeAddress"),
                    TelefonoCasa=F("idDonor__homePhone"),
                    DireccionTrabajo=F("idDonor__workAddress"),
                    TelefonoTrabajo=F("idDonor__workAddress"),
                    LugarNacimiento=F("idDonor__birthPlace"),
                    idEstadoDonador=F("idDonor__state"),
                    DescripcionEstadoDonador=F("idDonor__stateDescription"),
                    CantidadDonaciones=F("idDonor__donationAmount"),
                    FechaUltimaDonacion=F("idDonor__lastDonationDate"),
                    IdTipoSangre=F("idDonor__idBloodType"),
                    TipoSangre=F("idDonor__idBloodType__bloodType"),
                    MunicipioResidencia=F("idDonor__idCity__city"),
                    GrupoEtnico=F("idDonor__idEthnicGroup__ethnicGroup"),
                )
            )
            listDonations = list(donations)

            if len(listDonations) > 0:
                donacion = listDonations[0]
                donacion["EstadoDonacion"] = dict(DonationState.choices).get(
                    donacion["idEstadoDonacion"]
                )
                donacion["EstadoDonador"] = dict(DonorState.choices).get(
                    donacion["idEstadoDonador"]
                )
                donacion["Genero"] = dict(Gender.choices).get(donacion["idGenero"])

                data = {"message": "SUCCESS", "Donation": listDonations[0]}
            else:
                data = {"message": "Campaign Receiver not found...", "Donations": []}
            return JsonResponse(data)
        else:
            donations = list(
                Donation.objects.select_related(
                    "idDonationType", "idDonor__idPerson"
                ).values(
                    Id=F("id"),
                    Correlativo=F("correlative"),
                    Correlativo_Sangre=F("bloodCorrelative"),
                    Estado=F("state"),
                    Observaciones=F("comments"),
                    Peso=F("weight"),
                    Temperatura=F("temperature"),
                    Presion=F("bloodPressure"),
                    Hemoglobina=F("hemoglobin"),
                    IdJornada=F("idBloodDonationCampaign_id"),
                    IdTipoDonacion=F("idDonationType_id"),
                    IdDonor=F("idDonor_id"),
                    TipoDonacion=F("idDonationType__donationType"),
                    Nombre=F("idDonor__idPerson__firstName"),
                    Apellido=F("idDonor__idPerson__lastName"),
                    DPI=F("idDonor__idPerson__dpi"),
                    ID_Extranjero=F("idDonor__idPerson__idExtranjero"),
                )
            )
            if len(donations) > 0:
                datos = {"message": "SUCCESS", "Donations": donations}
            else:
                data = {"message": '"Donations not found...', "Donations": []}
        return JsonResponse(datos)

    # POST
    def post(self, request):
        jd = json.loads(request.body)
        Donation.objects.create(
            correlative=jd["correlative"],
            bloodCorrelative=jd["bloodCorrelative"],
            state=jd["state"],
            comments=jd["comments"],
            weight=jd["weight"],
            temperature=jd["temperature"],
            bloodPressure=jd["bloodPressure"],
            hemoglobin=jd["hemoglobin"],
            idBloodDonationCampaign_id=jd["idBloodDonationCampaign_id"],
            idDonationType_id=jd["idDonationType_id"],
            idDonor_id=jd["idDonor_id"],
        )
        datos = {"message": "SUCCESS"}
        return JsonResponse(datos)

    # PUT
    def put(self, request, id):
        jd = json.loads(request.body)
        listDonations = list(Donation.objects.filter(id=id).values())
        if len(listDonations) > 0:
            donation = Donation.objects.get(id=id)
            donation.bloodCorrelative = jd["bloodCorrelative"]
            donation.state = jd["state"]
            donation.comments = jd["comments"]
            donation.weight = jd["Weight"]
            donation.temperature = jd["Temperature"]
            donation.bloodPressure = jd["BloodPressure"]
            donation.hemoglobin = jd["Hemoglobin"]
            donation.idBloodCampaign_id = jd["idBloodCampaign"]
            donation.idDonationType_id = jd["idDonationType"]
            donation.idDonor_id = jd["idDonor"]
            donation.save()  # se guardan los cambios}

            if( jd["state"] == 1):
                donor = Donor.objects.get(id=jd["idDonor"])
                amount = donor.donationAmount 
                
                #Verificar logros
                achievments =Achievement.objects.values()
                if len(achievments)>0:
                    for row in achievments:
                        ach=Achievement.objects.get(id=row['id'])
                        donorAchievement = list(DonorAchievement.objects.filter(Q(idAchievement=row['id'])&Q(idDonor=jd['idDonor'])).values())
                        if len(donorAchievement)>0:
                            print(donorAchievement)
                        else:
                            if row['amount']==amount:
                                DonorAchievement.objects.create(
                                    idAchievement=ach,
                                    idDonor=donor
                                )



            datos = {"message": "Donation update successful"}
        else:
            datos = {"message": "Error, Donation group update"}
        return JsonResponse(datos)

    # DELETE
    def delete(self, request, id):
        listDonations = list(Donation.objects.filter(id=id).values())
        if len(listDonations) > 0:  # si existe tipo de usuario
            Donation.objects.filter(id=id).delete()
            datos = {"message": "DELETE, donation deleted"}
        else:  # no existe
            datos = {"message": "ERROR, not found Donation"}
        return JsonResponse(datos)


class GetDonationsCampaignView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0): 
        if id > 0:
            donations = list(
                Donation.objects.select_related("idDonationType", "idDonor__idPerson")
                .filter(idBloodDonationCampaign_id=id)
                .values(
                    Id=F("id"),
                    Correlativo=F("correlative"),
                    Correlativo_Sangre=F("bloodCorrelative"),
                    Estado=F("state"),
                    Observaciones=F("comments"),
                    Pesos=F("weight"),
                    Temperatura=F("temperature"),
                    Presion=F("bloodPressure"),
                    Hemoglobina=F("hemoglobin"),
                    IdJornada=F("idBloodDonationCampaign_id"),
                    IdTipoDonacion=F("idDonationType_id"),
                    IdDonor=F("idDonor_id"),
                    Tipo_Donacion=F("idDonationType__donationType"),
                    Nombre=F("idDonor__idPerson__firstName"),
                    Apellido=F("idDonor__idPerson__lastName"),
                    DPI=F("idDonor__idPerson__dpi"),
                    ID_Extranjero=F("idDonor__idPerson__idExtranjero"),
                )
            )

            if len(donations) > 0:
                data = {"message": "SUCCESS", "Donations": donations}
            else:
                data = {
                    "message": "1. Donations of campaign not found...",
                    "Donations": [],
                }
            return JsonResponse(data)
        else:
            data = {"message": "2. Donations of Campaign not found...", "Donations": []}
            return JsonResponse(data)


class updateStateDonationView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # PUT
    def put(self, request, id):
        jd = json.loads(request.body)
        listDonations = list(Donation.objects.filter(id=id).values())
        if len(listDonations) > 0:
            donation = Donation.objects.get(id=id)
            donation.state = jd["state"]
            donation.comments = jd["comments"]
            donation.save()  # se guardan los cambios
            datos = {"message": "Donation update successful"}
        else:
            datos = {"message": "Error, Donation group update"}
        return JsonResponse(datos)


class GetDonationsCompleteFalseView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            donations = list(
                Donation.objects.select_related()
                .filter(idBloodDonationCampaign_id=id, state=1, asignado=False)
                .values(
                    "id",
                    "bloodCorrelative",
                    "idBloodDonationCampaign",
                    "idDonationType",
                    "idDonor",
                    "asignado",
                    TipoSangre=F("idDonor__idBloodType__bloodType"),
                )
            )
            if len(donations) > 0:
                data = {"message": "SUCCESS", "Donations": donations}
            else:
                data = {
                    "message": "1. Donations of campaign not found...",
                    "Donations": [],
                }
            return JsonResponse(data)
        else:
            data = {"message": "2. Donations of Campaign not found...", "Donations": []}
            return JsonResponse(data)


class GetDonationsByDateView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self,req):
        
        jd=json.loads(req.body)
        start_date = timezone.make_aware(datetime.strptime(jd['startDate'], '%Y-%m-%d'))
        end_date = timezone.make_aware(datetime.strptime(jd['endDate'], '%Y-%m-%d'))
        donations = list(
                Donation.objects.select_related()
                .filter(created_at__range=(start_date,end_date+ timedelta(days=1)))
                .values(
                    'id', 'bloodCorrelative', 'idBloodDonationCampaign','idDonationType','created_at', 'idDonor__idPerson','idDonor__idPerson__gender',
                    Nombres=F('idDonor__idPerson__firstName'),
                    Apellidos=F('idDonor__idPerson__lastName'),
                    TipoSangre=F("idDonor__idBloodType__bloodType")
                )
            )
        print(donations)
        if len(donations) > 0:
            for i in donations:
                i['Género'] = dict(Gender.choices).get(i['idDonor__idPerson__gender'])
                del i['idDonor__idPerson__gender']
                i["Fecha"]=i['created_at'].strftime("%d-%m-%Y")
            data1 = {"Donations": donations}
        else:
            data1 = {
                "Donations": [],
            }
        personalDonations = list(PersonalDonation.objects.select_related().filter(_date__range=(jd['startDate'],jd['endDate'])).values(
            '_date',
            Nombres=F('idDonor__idPerson__firstName'),
            Apellidos=F('idDonor__idPerson__lastName'),
            TipoSangre=F("idDonor__idBloodType__bloodType"),
        ))
        if len(personalDonations)>0:
            for i in personalDonations:
                i["Fecha"]=i['_date'].strftime("%d-%m-%Y")
            data2 = {"Donations": personalDonations}
        else:
            data2 = {"Donations": []}
            
        data={"Donations": data1['Donations']+data2['Donations']}
        return JsonResponse(data)


class GetDonationsDonorView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            donations = list(
                Donation.objects.select_related("idDonationType", "idDonor__idPerson")
                .filter(idDonor_id=id)
                .values(
                    Id=F("id"),
                    Correlativo=F("correlative"),
                    Correlativo_Sangre=F("bloodCorrelative"),
                    Estado=F("state"),
                    Observaciones=F("comments"),
                    Pesos=F("weight"),
                    Temperatura=F("temperature"),
                    Presion=F("bloodPressure"),
                    Hemoglobina=F("hemoglobin"),
                    IdJornada=F("idBloodDonationCampaign_id"),
                    IdTipoDonacion=F("idDonationType_id"),
                    IdDonor=F("idDonor_id"),
                    Tipo_Donacion=F("idDonationType__donationType"),
                    Nombre=F("idDonor__idPerson__firstName"),
                    Apellido=F("idDonor__idPerson__lastName"),
                    DPI=F("idDonor__idPerson__dpi"),
                    ID_Extranjero=F("idDonor__idPerson__idExtranjero"),
                    Fecha=F("idBloodDonationCampaign___date"),
                    LugarJornada=F("idBloodDonationCampaign__place"),
                )
            )

            if len(donations) > 0:
                data = {"message": "SUCCESS", "Donations": donations}
            else:
                data = {
                    "message": "1. Donations of campaign not found...",
                    "Donations": [],
                }
            return JsonResponse(data)
        else:
            data = {"message": "2. Donations of Campaign not found...", "Donations": []}
            return JsonResponse(data)

