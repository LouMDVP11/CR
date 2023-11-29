from django.http.response import JsonResponse
from django.views import View
from ..models import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import F


class DonationReceiverCampaignView(View):
    @method_decorator(csrf_exempt)  # Saltamos restriccion
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, req, id=0):
        id = int(id)
        if id > 0:
            donationsReceiver = list(
                DonationReceiverCampaign.objects.filter(id=id).values()
            )
            if len(donationsReceiver) > 0:
                donationReceiver = donationsReceiver[0]
                data = {
                    "message": "SUCCESS",
                    "DonationReceiverCampaign": donationReceiver,
                }
            else:
                data = {
                    "message": "ERROR, donationsReceiver not found...",
                    "DonationReceiverCampaign": [],
                }
            return JsonResponse(data)
        else:
            donationsReceiver = list(DonationReceiverCampaign.objects.values())
            if len(donationsReceiver) > 0:
                data = {
                    "message": "SUCCESS",
                    "DonationReceiverCampaign": donationsReceiver,
                }
            else:
                data = {
                    "message": "ERROR, donationsReceiver not found...",
                    "DonationReceiverCampaign": [],
                }
            return JsonResponse(data)

    def post(self, req):
        jd = json.loads(req.body)
        DonationReceiverCampaign.objects.create(idDonation_id = jd["idDonation_id"], idReceiverCampaign_id = jd["idReceiverCampaign_id"])
        data = {"message": "SUCCESS"}
        return JsonResponse(data)

    def delete(self, req, id):
        donationsReceiver = list(
            DonationReceiverCampaign.objects.filter(id=id).values()
        )
        if len(donationsReceiver)  > 0:
            DonationReceiverCampaign.objects.filter(id=id).delete()
            data = {"message": "DonationReceiverCampaign deleted"}
        else:
            data = {"message": "ERROR, donationReceiver not found"}
        return JsonResponse(data)


class DonationIDReceiverView(View):
    @method_decorator(csrf_exempt)  # Saltamos restriccion
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, req, id=0):
        id = int(id)
        if id > 0:
            donationsReceiver = list(
                DonationReceiverCampaign.objects.filter(
                    idReceiverCampaign_id=id
                ).values(
                    "id",
                    "idDonation_id",
                    "idReceiverCampaign_id",
                    TipoSangre=F("idDonation__idDonor__idBloodType__bloodType"),
                    Correlativo=F("idDonation__bloodCorrelative"),
                )
            )
            if len(donationsReceiver) > 0:
                donationReceiver = donationsReceiver
                data = {
                    "message": "SUCCESS",
                    "DonationReceiverCampaign": donationReceiver,
                }
            else:
                data = {
                    "message": "ERROR, donationsReceiver not found...",
                    "DonationReceiverCampaign": [],
                }
            return JsonResponse(data)
        else:
            data = {
                "message": "ERROR, donationsReceiver not found...",
                "DonationReceiverCampaign": [],
            }
            return JsonResponse(data)
