from django.http.response import JsonResponse
from django.views import View
from ..models import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import IntegrityError


class ReceiverView(View):
    @method_decorator(csrf_exempt)  # Saltamos restriccion
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, req, id=0):
        id = int(id)
        if (id > 0):
            recievers = list(Receiver.objects.filter(id=id).values("id","receiverName", "address", "telephone", "state","dpiPatient","email","idExtranjero","observations","idCity_id","idCity_id__idProvince_id"))
            if len(recievers) > 0:
                receiver = recievers[0]
                data = {'message': "SUCCESS", 'Receiver': receiver}
            else:
                data = {'message': "ERROR, Receivers not found...", "Receiver":[]}
            return JsonResponse(data)
        else:
            recievers = list(Receiver.objects.values())
            if len(recievers) > 0:
                data = {'message': "SUCCESS", 'Recievers': recievers}
            else:
                data = {'message': "ERROR, receivers not found...", "Recievers":[]}
            return JsonResponse(data)

    def post(self, req):
        jd = json.loads(req.body)
        try:
            # Intenta crear un nuevo receptor
            Receiver.objects.create(
                address=jd['address'],
                receiverName=jd['receiverName'],
                telephone=jd['telephone'],
                email=jd['email'],
                observations=jd['observations'],
                dpiPatient=jd['dpiPacient'],
                idExtranjero=jd['idExtranjero'],
                idCity_id=jd['idCity']
            )
            data = {'message': "SUCCESS"}
        except IntegrityError as e:
            # Si se produce una excepción de integridad, significa que ya existe un receptor con el mismo receiverName o dpiPatient
            data = {
                "message": "ERROR",
                "error_message": "El receiverName o dpiPatient ya existe en la base de datos."
            }

        return JsonResponse(data)

    def put(self, req, id):
        jd = json.loads(req.body)
        receivers = list(Receiver.objects.filter(id=id).values())
        if len(receivers) > 0:
            receiver = Receiver.objects.get(id=id)
            receiver.receiverName = jd['receiverName']
            receiver.address = jd['address']
            receiver.telephone = jd['telephone']
            receiver.email = jd['email']
            receiver.observations = jd['observations']
            receiver.dpiPatient = jd['dpiPatient']
            receiver.idExtranjero = jd['idExtranjero']
            receiver.idCity = City.objects.get(id=jd['idCity'])
            receiver.save()
            datos = {"message": "Receiver successfully edited"}
        else:
            datos = {"message": "Receiver not found to edit"}
        return JsonResponse(datos)

    def delete(self, id):
        receivers = list(Receiver.objects.filter(id=id).values())
        if receivers > 0:
            Person.objects.filter(id=id).delete
            data = {'message': "Receiver deleted"}
        else:
            data = {'message': "ERROR, receiver not found"}
        return JsonResponse(data)

class ReceiverNoAsignadosView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, req, id=0):
        id = int(id)

        receptores_asignados = CampaignReceiver.objects.filter(idBloodDonationCampaign_id=id).values_list(
            'idReceiver_id', flat=True)

        # Modifica la consulta para excluir receptores con estado 2
        receptores_no_asignados = Receiver.objects.exclude(id__in=receptores_asignados).exclude(state=2).values()

        if len(receptores_no_asignados) > 0:
            data = {'message': "SUCCESS", 'Recievers': list(receptores_no_asignados)}
        else:
            data = {'message': "ERROR, receivers not found...", 'Recievers': []}

        return JsonResponse(data)

class UpdateStateView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def put(self, request, id):
        jd = json.loads(request.body)
        receptores = list(Receiver.objects.filter(id=id).values())
        if len(receptores) > 0:
            receptores = Receiver.objects.get(id=id)
            receptores.state = (jd["state"])
            receptores.save()  # se guardan los cambios
            datos = {"message": "Receptor update successful"}
        else:
            datos = {"message": "Error, Receptor group update"}
        return JsonResponse(datos)    