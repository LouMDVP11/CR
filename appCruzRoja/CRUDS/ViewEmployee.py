from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from ..models import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import F, Value
from django.db.models.functions import Concat

# ------------------------------------------------ CRUD DE Employed ---------------------------------------------------------
class EmployeeView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # GET
    def get(self, request, id=0):
        if id > 0:
            listEmployees = (
                Employee.objects.select_related("idPerson", "idPosition")
                .filter(id=id)
                .values(
                    idEmpleado=F("id"),
                    idPuesto=F("idPosition__id"),
                    idPersona=F("idPerson__id"),
                    Nombre=F("idPerson__firstName"),
                    Apellido=F("idPerson__lastName"),
                    DPI=F("idPerson__dpi"),
                    Correo=F("idPerson__email"),
                    Fecha_de_Nacimiento=F("idPerson__birthDate"),
                    Puesto=F("idPosition__position"),
                    Estado=F("state"),
                    Usuario=F("idPerson__user"),
                    tipo = F("idPerson__userType"),
                )
            )

            # Convierte el queryset en una lista de diccionarios
            listEmployees = list(listEmployees)

            if len(listEmployees) > 0:
                datos = {"message": "SUCCESS", "Employee": listEmployees}
            else:
                datos = {"message": "ERROR, Employee no found", "Employee": []}
            return JsonResponse(datos)

        else:
            listEmployees = list(
                Employee.objects.select_related("idPerson", "idPosition").values(
                    idEmpleado=F("id"),
                    idPuesto=F("idPosition__id"),
                    idPersona=F("idPerson__id"),
                    NombreCompleto=Concat(F("idPerson__firstName"), Value(' '), F("idPerson__lastName")),
                    Nombre=F("idPerson__firstName"),
                    Apellido=F("idPerson__lastName"),
                    DPI=F("idPerson__dpi"),
                    Correo=F("idPerson__email"),
                    Fecha_de_Nacimiento=F("idPerson__birthDate"),
                    Puesto=F("idPosition__position"),
                    Estado=F("state"),
                    Usuario=F("idPerson__user"),
                    tipo = F("idPerson__userType"),
                )
            )
            #            listEmployees = list(Employee.objects.values())
            if len(listEmployees) > 0:
                datos = {"message": "SUCCESS", "Employee": listEmployees}
            else:
                datos = {"message": "ERROR,List of Employee not found", "Employee": []}
            return JsonResponse(datos)

    # POST
    def post(self, request):
        jd = json.loads(request.body)
        Employee.objects.create(
            idPerson_id=jd["idPerson_id"], idPosition_id=jd["idPosition_id"]
        )
        datos = {"message": "SUCCESS, Employee created"}
        return JsonResponse(datos)

    # PUT
    def put(self, request, id):
        jd = json.loads(request.body)
        listEmployees = list(Employee.objects.filter(id=id).values())
        if len(listEmployees) > 0:
            employee = Employee.objects.get(id=id)
            employee.idPerson_id = jd["idPerson_id"]
            employee.idPosition_id = jd["idPosition_id"]
            employee.state = jd["state"]
            employee.save()  # se guardan los cambios
            datos = {"message": "Employee update successful", "Employee": employee.state}
        else:
            datos = {"message": "Error, Employee group update"}
        return JsonResponse(datos)

    # DELETE
    def delete(self, request, id):
        listEmployees = list(Employee.objects.filter(id=id).values())
        if len(listEmployees) > 0:  # si existe tipo de usuario
            Employee.objects.filter(id=id).delete()
            datos = {"message": "DELETE, employee deleted"}
        else:  # no existe
            datos = {"message": "ERROR, not found Employee"}
        return JsonResponse(datos)
