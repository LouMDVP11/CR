from django.http.response import JsonResponse
from django.views import View
from ..models import *
import bcrypt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
import json
from django.db.models import F
from django.db import IntegrityError
from django.contrib.auth import login
from django.http import HttpResponse




# TEST COMMENT
class PersonView(View):
    @method_decorator(csrf_exempt)  # Saltamos restriccion
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, req, id=0):
        id = int(id)
        if id > 0:
            people = list(Person.objects.filter(id=id).values())
            if len(people) > 0:
                person = people[0]
                data = {"message": "SUCCESS", "Persona": person}
            else:
                data = {"message": "ERROR, person not found..."}
            return JsonResponse(data)
        else:
            people = list(Person.objects.values())
            if len(people) > 0:
                # print(people[32])
                data = {
                    "message": "SUCCESS",
                    "Cantidad de datos": len(people),
                    "People": sorted(people, key=lambda x: x["id"]),
                }
            else:
                data = {"message": "ERROR, people not found..."}
            return JsonResponse(data)

    def post(self, req):
        jd = json.loads(req.body)
        try:
            hashed_password = bcrypt.hashpw(
                jd["_password"].encode("utf-8"), bcrypt.gensalt()
            )
            #print(jd["dpi"], ".", len(jd["dpi"]), ".")
            dpi_=''
            if(jd["dpi"]!=None):
                if(len(jd["dpi"])==0):
                    dpi_=None
                else:
                    dpi_=jd["dpi"]
            else:
                dpi_=None
            idex_=''
            if(jd["idExtranjero"]!=None):
                if(len(jd["idExtranjero"])==0):
                    idex_=None
                else:
                    idex_=jd["idExtranjero"]
            else:
                idex_=None
            newPerson = Person.objects.create(
                dpi=dpi_,
                idExtranjero=idex_,
                firstName=jd["firstName"],
                lastName=jd["lastName"],
                user=jd["user"],
                _password=hashed_password.decode("utf-8"),
                email=jd["email"],
                gender=jd["gender"],
                birthDate=jd["birthDate"],
                userType=jd["userType"],
            )
            print("OK?")
            data = {
                "message": "SUCCESS",
                "Persona": newPerson.id,
                "Persona_dpi": newPerson.dpi,
                "Persona_idex": newPerson.idExtranjero,
            }
            return JsonResponse(data)
        except IntegrityError:
            data = {
                "message": "ERROR",
                "error_message": "Hay información ya existente con el DPI, el otro tipo de identificador o correo en la base de datos."
            }
            return JsonResponse(data)
            
    def delete(self, id):
        people = list(Person.objects.filter(id=id).values())
        if people > 0:
            Person.objects.filter(id=id).delete
            data = {"message": "Person deleted"}
        else:
            data = {"message": "ERROR, person not found"}
        return JsonResponse(data)

    def put(self, req, id):
        jd = json.loads(req.body)
        people = list(Person.objects.filter(id=id).values())
        if len(people) > 0:
            person = Person.objects.get(id=id)
            person.dpi = jd["dpi"]
            person.idExtranjero = jd["idExtranjero"]
            person.firstName = jd["firstName"]
            person.lastName = jd["lastName"]
            person.user = jd["user"]
            person._password = jd["_password"]
            person.email = jd["email"]
            person.gender = jd["gender"]
            person.birthDate = jd["birthDate"]
            person.userType = jd["userType"]
            person.save()
            data = {"message": "SUCCESS"}
        else:
            data = {"message": "ERROR, person not found"}
        return JsonResponse(data)

class UpdateUserView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, req, id):
        jd = json.loads(req.body)
        people = list(Person.objects.filter(id=id).values())
        print(people)
        if len(people) > 0:
            person = Person.objects.get(id=id)
            person.user = jd["user"]
            person.save()
            data = {"message": "SUCCESS"}
        else:
            data = {"message": "ERROR, person not found"}
        return JsonResponse(data)
class VerifyPasswordView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, req, id):
        id = int(id)
        jd = json.loads(req.body)
        
        people = list(Person.objects.filter(id=id).values())
        if len(people) > 0:
            person = Person.objects.get(id=id)
            if bcrypt.checkpw(jd['apassword'].encode('utf-8'), person._password.encode('utf-8')):
                hashed_password = bcrypt.hashpw(
                    jd["npassword"].encode("utf-8"), bcrypt.gensalt()
                )
                print(person)
                person._password=hashed_password.decode("utf-8")
                person.save()
                data = {"message": "SUCCESS"}
            else:
                data = {"message": "Contraseña actual incorrecta."}
        else:
            data = {"message": "Error al cambiar la contraseña."}
        return JsonResponse(data)
    
class UpdatePersonNoPassword(View):
    @method_decorator(csrf_exempt)  # Saltamos restriccion
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, req, id):
        jd = json.loads(req.body)
        people = list(Person.objects.filter(id=id).values())
        print(people)
        if len(people) > 0:
            person = Person.objects.get(id=id)
            person.firstName = jd["firstName"]
            person.lastName = jd["lastName"]
            person.gender = jd["gender"]
            person.email = jd["email"]
            person.save()
            data = {"message": "SUCCESS"}
        else:
            data = {"message": "ERROR, person not found"}
        return JsonResponse(data)

    def put(self, req, id):
        jd = json.loads(req.body)
        people = list(Person.objects.filter(id=id).values())
        if len(people) > 0:
            person = Person.objects.get(id=id)
            person.dpi = jd["dpi"]
            person.firstName = jd["firstName"]
            person.lastName = jd["lastName"]
            #person.user = jd["user"]
            #person.email = jd["email"]
            person.gender = jd["gender"]
            person.birthDate = jd["birthDate"]
            person.userType = jd["userType"]
            person.save()
            data = {"message": "Persona editada"}
        else:
            data = {"message": "ERROR, person not found"}
        return JsonResponse(data)

class getAllData(View):
    @method_decorator(csrf_exempt)  # Saltamos restriccion
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, req, id):
        people = list(Person.objects.filter(id=id).values())
        if len(people) > 0:
            person = people[0]
            person["gender"] = dict(Gender.choices).get(person["gender"])
            donors = (
                Donor.objects.filter(idPerson=id)
                .select_related(
                    "idBloodType", "idEthnicGroup", "idCity", "idCity__idProvince"
                )
                .values(
                    "id",
                    "idBloodType__bloodType",
                    "idBloodType__id",
                    "idCity__city",
                    "idCity__idProvince__province",
                    "idEthnicGroup__ethnicGroup",
                    "idPerson__email",
                    "homeAddress",
                    "homePhone",
                    "workAddress",
                    "workPhone",
                    "birthPlace",
                    "stateDescription",
                    "state",
                    "idPerson__birthDate",
                    "donationAmount",
                    "lastDonationDate"
                )
            )
            if len(donors) > 0:
                donor = donors[0]
                
                donor["donorState"] = dict(DonorState.choices).get(donor["state"])
                del donor["state"]
                donor["idDonor"] = donor["id"]
                del donor["id"]
                donor["fechaNac"] = donor["idPerson__birthDate"].strftime("%d-%m-%Y")
            else:
                donor = {}
            employees = list(
                Employee.objects.filter(idPerson=id)
                .select_related("idPosition")
                .values("idPosition","idPosition__position", "state", "id")
            )
            if len(employees) > 0:
                employee = employees[0]
                employee["employeeState"] = dict(EmployeeState.choices).get(
                    employee["state"]
                )
                employee["employeeSt"]=employee['state']
                del employee["state"]
                employee["idEmployee"] = employee["id"]
                del employee["id"]
            else:
                employee = {}
            merged_data = {**person, **donor, **employee}
            datos = {"message": "SUCCESS", "Person": merged_data}
        else:
            datos = {"message": "ERROR", "Person": []}
        return JsonResponse(datos)

class VerifyUserPassword(View):
    @method_decorator(csrf_exempt)  # Saltamos restriccion
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, req, id):
        jd = json.loads(req.body)
        people = list(Person.objects.filter(id=id).values())
        if len(people) > 0:
            person = Person.objects.get(id=id)
            password_matches = bcrypt.checkpw(
                jd["_password"].encode("utf-8"), person._password.encode("utf-8")
            )
            if password_matches:
                data = {"message": "SUCCESS"}
            else:
                data = {"message": "ERROR", "Data": "Contraseña incorrecta"}
        else:
            data = {"message": "ERROR", "Data": "No encuentro url"}
        print(data)
        return JsonResponse(data)

class UpdateTypeView(View):
    @method_decorator(csrf_exempt)  # Saltamos restriccion
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def put(self, req, id):
        jd = json.loads(req.body)
        people = list(Person.objects.filter(id=id).values())
        if len(people) > 0:
            person = Person.objects.get(id=id)
            person.userType = jd["userType"]
            person.save()
            data = {"message": "El tipo de la persona ha sido editada"}
        else:
            data = {"message": "ERROR, person not found"}
        return JsonResponse(data)

class selectLastIdView(View):
    @method_decorator(csrf_exempt)  # Saltamos restricción CSRF
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, req):
        try:
            latest_person = Person.objects.latest("id")
            data = {
                "lastId": latest_person.id,
            }
        except Person.DoesNotExist:
            data = {"message": "ERROR, person not found..."}

        return JsonResponse(data)

class searchByDPI(View):
    @method_decorator(csrf_exempt)  # Saltamos restricción CSRF
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, req, id=0):
        id = int(id)
        if id > 0:
            people = list(Person.objects.filter(dpi=id).values())
            if len(people) > 0:
                person = people[0]
                data = {"message": "SUCCESS", "Person": person}
            else:
                data = {"message": "ERROR, person not found...","Person": []}
            return JsonResponse(data)
        else:
            data = {"message": "ERROR, people not found...", "Person": []}
            return JsonResponse(data)
        
class UpdateCredentialsUser(View):
    @method_decorator(csrf_exempt)  # Saltamos restricción CSRF
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)     
    
    def put(self, req, id):
        jd = json.loads(req.body)
        people = list(Person.objects.filter(id=id).values())
        if len(people) > 0:
            person = Person.objects.get(id=id)

            # Hash the new password
            hashed_password = bcrypt.hashpw(jd["_password"].encode("utf-8"), bcrypt.gensalt())

            person._password =hashed_password.decode("utf-8")
            person.user = jd["user"]
            person.save()
            data = {"message": "Credenciales asignadas correctamente"}
        else:
            data = {"message": "ERROR, person not found"}
        return JsonResponse(data) 

class searchByIdExtranjero(View):
    @method_decorator(csrf_exempt)  # Saltamos restricción CSRF
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, req, id="0"):
        try:
            id = str(id)
        except ValueError:
            data = {"message": "ERROR","Person": []}
            return JsonResponse(data)        

        people = list(Person.objects.filter(idExtranjero=id).values())
        if len(people) > 0:
            person = people[0]
            data = {"message": "SUCCESS", "Person": person}
        else:
            data = {"message": "ERROR","Person": []}
        return JsonResponse(data)

class PersonSignIn(View):
    @method_decorator(csrf_exempt)  # Saltamos restriccion
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, req):
        jd = json.loads(req.body)
        val = 1
        try:
            people = list(Person.objects.filter(user=jd['user']).values())
            if len(people) > 0:
                person = people[0]
                #print(check_password("Admin12345&", person['_password']))
                print(bcrypt.checkpw(jd['_password'].encode('utf-8'), person['_password'].encode('utf-8')))
                      
                if bcrypt.checkpw(jd['_password'].encode('utf-8'), person['_password'].encode('utf-8')):
                    donors = (
                        Donor.objects.filter(idPerson=person['id'])
                        .values()
                    )
                    if len(donors) > 0:
                        donor = donors[0]
                        donor["idDonor"] = donor["id"]
                        del donor["id"]
                    else:
                        donor = {}
                    employees = list(
                        Employee.objects.filter(idPerson=person['id'])
                        .values("id", "rol", "state")
                    )
                    if len(employees) > 0:
                        employee = employees[0]
                        employee["idEmployee"] = employee["id"]
                        employee["employeeState"] = employee["state"]
                        del employee["id"]
                        del employee["state"]
                        if employee["employeeState"]!=1:
                            val=0
                    else:
                        employee = {}
                    merged_data = {**person, **donor, **employee}
                    if(val==0):
                         data = {
                        "message": "ERROR",
                        "error_message": "ERROR, usuario inhabilitado."
                        }
                    else:
                        data = {
                            "message": "ÉXITO",
                            "error_message": "Inicio de sesión exitoso",
                            "person":merged_data
                        }
                else:
                    data = {
                        "message": "ERROR",
                        "error_message": "Usuario y/o contraseña incorrectos."
                    }
            else:
                data = {"message": "ERROR", "error_message": "ERROR, usuario y/o contraseña incorrectos."}
            return JsonResponse(data)
        except IntegrityError:
            data = {
                "message": "ERROR",
                "error_message": "Error al intentar iniciar sesión."
            }
            return JsonResponse(data)
        
class UpdateEmployeeNoPassword(View):
    @method_decorator(csrf_exempt)  # Saltamos restriccion
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def put(self, req, id):
        jd = json.loads(req.body)
        people = list(Person.objects.filter(id=id).values())
        if len(people) > 0:
            person = Person.objects.get(id=id)
            person.dpi = jd["dpi"]
            person.firstName = jd["firstName"]
            person.lastName = jd["lastName"]
            person.gender = jd["gender"]
            person.birthDate = jd["birthDate"]
            person.save()
            data = {"message": "Persona editada"}
        else:
            data = {"message": "ERROR, person not found"}
        return JsonResponse(data)
    
class PostPerson(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, req):
        jd = json.loads(req.body)

        try:
            dpi_ = ''
            if jd.get("dpi") is not None:
                if len(jd["dpi"]) == 0:
                    dpi_ = None
                else:
                    dpi_ = jd["dpi"]
            else:
                dpi_ = None

            idex_ = ''
            if jd.get("idExtranjero") is not None:
                if len(jd["idExtranjero"]) == 0:
                    idex_ = None
                else:
                    idex_ = jd["idExtranjero"]
            else:
                idex_ = None
            newPerson1 = Person.objects.create(
                dpi=dpi_,
                idExtranjero=idex_,
                firstName=jd["firstName"],
                lastName=jd["lastName"],
                gender=jd["gender"],
                email=jd["email"],
                birthDate=jd["birthDate"],
                userType=jd["userType"],
            )
            print(newPerson1)
            data = {
                "message": "SUCCESS",
                "PeopleId": newPerson1.id,
                "Persona_dpi": newPerson1.dpi,
                "Persona_idex": newPerson1.idExtranjero,
            }
            return JsonResponse(data)
        except IntegrityError as e:
            print(f"IntegrityError: {e}")
            data = {
                "message": "ERROR",
                "error_message": "Hay información ya existente en la base de datos_."
            }
            return JsonResponse(data)

        
class PersonRecoveryView(View):
    @method_decorator(csrf_exempt) 
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, req):
        jd=json.loads(req.body)
        people = list(Person.objects.filter(user=jd['username'], email=jd['email']).values())
        print(people)
        try:
            if(len(people)>0):
                person = Person.objects.get(user=jd['username'], email=jd['email'])
                hashed_password = bcrypt.hashpw(
                    jd["_password"].encode("utf-8"), bcrypt.gensalt()
                )
                person._password=hashed_password.decode("utf-8")
                person.save()
                print(person.firstName)
                personSend={
                    "firstName":person.firstName,
                    "lastName":person.lastName,
                    "email":person.email
                }
                data = {"message": "OK", "person":personSend}
                return JsonResponse(data)
            else:
                data = {"message": "ERROR, datos incorrectos. "}
                return JsonResponse(data)
        except Exception:
            data = {"message": "ERROR, datos incorrectos."}
            return JsonResponse(data)
            
class SearchByDPIorIdView(View):
    @method_decorator(csrf_exempt)  # Saltamos restricción CSRF
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, req):
        jd=json.loads(req.body)
        print(jd)
        dpi_=''
        if(jd["dpi"]!=None):
            if(len(jd["dpi"])==0):
                dpi_=None
            else:
                dpi_=jd["dpi"]
        else:
            dpi_=None
        idex_=''
        if(jd["idExtranjero"]!=None):
            if(len(jd["idExtranjero"])==0):
                idex_=None
            else:
                idex_=jd["idExtranjero"]
        else:
            idex_=None
        if(idex_==None):
            people = list(Person.objects.filter(dpi=jd["dpi"]).values())
        elif(dpi_==None):
            people = list(Person.objects.filter(idExtranjero=jd["idExtranjero"]).values())
        elif(dpi_!=None and idex_!=None):
            people = list(Person.objects.filter(idExtranjero=jd["idExtranjero"], dpi=jd["dpi"]).values())

        if len(people) > 0:
            person = people[0]
            if person['user']!=None:
                if len(person['user'])>0:
                    data = {"message": "ERROR, ya hay una persona registrada con esos datos..."}
                else:
                    data = {"message": "SUCCESS", "Person": person}
            else:
                data = {"message": "SUCCESS", "Person": person}
        else:
            data = {"message": "ERROR, no se encontraron personas con esos datos..."}
        return JsonResponse(data)
       
            
    