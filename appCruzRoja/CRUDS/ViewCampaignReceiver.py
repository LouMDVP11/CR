from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from ..models import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import F


# ------------------------------------------------ CRUD Campaign---------------------------------------------------------
class CampaignReceiverView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            listCampaigns = list(CampaignReceiver.objects.filter(id=id).values())
            if len(listCampaigns) > 0:
                campaign = listCampaigns[0]
                data = {"message": "SUCCESS", "CampaignReceiver": campaign}
            else:
                data = {
                    "message": "Campaign Receiver not found...",
                    "CampaignReceiver": [],
                }
            return JsonResponse(data)

        else:
            listCampaigns = list(CampaignReceiver.objects.values())
            if len(listCampaigns) > 0:
                data = {"CampaignReceivers": listCampaigns}
            else:
                data = {
                    "message": '"Campaign Receiver not found...',
                    "CampaignReceivers": [],
                }
            return JsonResponse(data)

    def post(self, request):
        jd = json.loads(request.body)
        # campaignFind = BloodDonationCampaign.objects.get(id=jd['idBloodDonationCampaign'])
        # receiverFind= Receiver.objects.get(id=jd['idReceiver'])
        campaign = CampaignReceiver.objects.create(
            bloodUnitsReceived=jd["bloodUnitsReceived"],
            purpose=jd["purpose"],
            idReceiver_id=jd["idReceiver"],
            idBloodDonationCampaign_id=jd["idBloodDonationCampaign"],
        )
        data = {
            "message": "SUCCESS, campaign receiver created",
            "CampaignReceiverId": campaign.id,
        }
        return JsonResponse(data)

        # PUT

    def put(self, request, id):
        jd = json.loads(request.body)
        listCampaignReceivers = list(
            CampaignReceiver.objects.filter(id=id).values()
        )  # uno en especifico
        if len(listCampaignReceivers) > 0:
            campaignR = CampaignReceiver.objects.get(id=id)
            campaignR.bloodUnitsReceived = jd["bloodUnitsReceived"]
            campaignR.purpose = jd["purpose"]
            campaignR.idReceiver = jd["idReceiver"]
            campaignR.idBloodDonationCampaign = jd["idBloodDonationCampaign"]
            campaignR.save()
            data = {"message": "Campaign Receiver successfully edited"}
        else:
            data = {"message": "Error, Campaign Receiver not found to edit"}
        return JsonResponse(data)

    # DELETE
    def delete(self, request, id):
        listCampaignReceivers = list(CampaignReceiver.objects.filter(id=id).values())
        if len(listCampaignReceivers) > 0:  # si existe tipo de usuario
            CampaignReceiver.objects.filter(id=id).delete()
            data = {"message": "SUCCESS"}
        else:  # no existe
            data = {"message": "ERROR"}
        return JsonResponse(data)


class ReceiverOfCampaignView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            listCampaigns = list(
                CampaignReceiver.objects.filter(idBloodDonationCampaign_id=id)
                .select_related("idPerson", "idPosition")
                .values(
                    Id=F("id"),
                    Unidades_de_sangre=F("bloodUnitsReceived"),
                    Proposito=F("purpose"),
                    IdCampaign=F("idBloodDonationCampaign"),
                    idReceptor=F("idReceiver"),
                    Receptor=F("idReceiver__receiverName"),
                )
            )
            if len(listCampaigns) > 0:
                data = {"message": "SUCCESS", "CampaignReceiver": listCampaigns}
            else:
                data = {
                    "message": "Campaign Receiver not found...",
                    "CampaignReceiver": [],
                }
            return JsonResponse(data)
        else:
            data = {"message": "Campaign Receiver not found...", "CampaignReceiver": []}
            return JsonResponse(data)
