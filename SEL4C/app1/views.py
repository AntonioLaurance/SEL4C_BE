from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.contrib.auth.hashers import check_password
from django.views.defaults import page_not_found
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.template import RequestContext
from django.db.models import Q
from app1.models import *
from app1.serializers import *
from app1.forms import *
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from json import loads, dumps
import sqlite3
import os

# --------------------------------------------------------------------
# Create your views here.
# --------------------------------------------------------------------
# Authentificate users in external sites
# This functions with the HTTP verb 'POST'

@csrf_exempt
def auth(request: HttpRequest):
    # Deserialization
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)

    # Authentification with given credentials autenticate(username = body["username"], password = body["password"])
    user = authenticate(request, username = body["username"], password = body["password"])

    if user is None:
        # The backend no authenticated the credentials
        json = {'detail': 'Invalid credentials'}

    else:
        # Init the session
        login(request, user)

        # The backend authenticated the credentials
        json = {'username': user.__getattribute__("username"),
                'pass_phase': user.__getattribute__("pass_phase"),
                'email': user.get_username(),   

                'personal_info': {
                    'name': user.__getattribute__("first_name"), 
                    'first_surname': user.__getattribute__("last_name"),
                    'second_surname': user.__getattribute__("second_last_name"),
                    'age': user.__getattribute__("age"),
                    'genre': user.__getattribute__("genre"),
                    'contry': user.__getattribute__("country"),
                },

                'important_dates': {
                    'date_joined': user.__getattribute__("date_joined").__str__(),
                    'last_login': user.__getattribute__("last_login").__str__(),

                },

                'academic_info': {
                    'institution': user.__getattribute__("institution"),
                    'grade': user.__getattribute__("grade"),
                    'carrer': user.__getattribute__("carrer")
                },
                
                'time_spended': user.__getattribute__("time_spended").__str__(),
                'verified_at': user.__getattribute__("verified_at").__str__(),
                'HMAC_hash': user.get_session_auth_hash()}        
    
    return HttpResponse(dumps(json), content_type = 'application/json')


@csrf_exempt
def register(request: HttpRequest):
    if request.method == 'POST':
        # Deserializa el cuerpo de la solicitud JSON
        body_unicode = request.body.decode('utf-8')
        body = loads(body_unicode)

        # Verifica si ya existe un usuario con el mismo correo electrónico
        if get_user_model().objects.filter(email = body["email"]).exists():
            return JsonResponse({"error": "El correo electrónico ya está registrado."}, status=400)
        
        # Crea un nuevo usuario con nombre de usuario basado en el correo electrónico
        user = get_user_model()(email = body["email"], password = body["password"])

        # Guarda el usuario en la base de datos
        user.save()

        # Devuelve una respuesta exitosa
        return JsonResponse({"message": "Usuario registrado exitosamente."}, status=201)


    else:
        # Devuelve una respuesta de error 401 para solicitudes que no sean POST
        return JsonResponse({"error": "Acceso no autorizado."}, status=401)


"""
@csrf_exempt
def auth(request: HttpRequest):
    # Deserializa el cuerpo de la solicitud JSON
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)

    print("JSON recibido:", body)  # Imprime el JSON que se recibió

    # Busca el usuario por su nombre de usuario o correo electrónico (puedes ajustarlo según tu modelo)
    user = User.objects.filter(Q(username=body["username"]) | Q(email=body["username"])).first()

    if user is None:
        print("Usuario no encontrado")
        # Si el usuario no existe, devuelve un error
        return HttpResponse(status=401)  # Cambiamos el código de estado a 401

    # Verifica la contraseña
    if check_password(body["password"], user.password):
        print("Contraseña válida")
        # Si la contraseña coincide, puedes devolver los datos del usuario
        json_data = {
            'username': user.username,
            'email': user.email,
            # Agrega otros campos del usuario aquí
        }
        return JsonResponse(json_data)

    print("Contraseña no válida")
    # Si la contraseña no coincide, devuelve un error
    return HttpResponse(status=401)  # Cambiamos el código de estado a 401
"""

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be created or viewed.
    """
    queryset = User.objects.all().order_by('date_joined')
    serializer_class = UserSerializer
    permission_clases = [permissions.AllowAny]

class HomeUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = HomeUser.objects.all().order_by('created_at')    # Set the queryset for the view
    serializer_class = HomeUserSerializer                       # Set the serializer class 
    permission_classes = [permissions.IsAuthenticated]          # Set the permission classes

class SessionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Session.objects.all().order_by('date_init')
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAdminUser]

class SurveyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [permissions.AllowAny]

class DeliverViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Deliver.objects.all().order_by('id')
    serializer_class = DeliverSerializer
    permission_classes = [permissions.AllowAny]

class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_clases = [permissions.AllowAny]

class AnswerQuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited. It's connected with API '\\respuestas'.
    """
    queryset = AnswerQuestion.objects.all()
    serializer_class = AnswerQuestionSerializer 
    permission_clases = [permissions.AllowAny]
    
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

# Home page    
def index(request: HttpRequest):
    if (request.user.is_staff):
        return render(request, 'menuadmin.html')
    else:
        return render(request, 'index.html')

# Contact page
def contacto(request):
    return render(request, 'contacto.html')

# En la carpeta 'documents/'
@csrf_exempt
def UploadFile(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print(form.fields['user'])
            return HttpResponse('The file is saved')
    else:
        form = BlogForm()
    context = {'form': form,}
    return render(request, 'upload.html', context)

# Se crea una carpeta por usuario en caso de que no la haya
# En la carpeta 'media/'
@csrf_exempt
def simple_upload(request):
    if request.method == 'POST' and request.FILES['file']:
        usuario = (request.POST['user'])
        actividad = (request.POST['activity'])
        nombre_evidencia = (request.POST['evidence_name'])
        myfile = request.FILES['file']
        fs = FileSystemStorage()
        path = os.path.join(fs.location, usuario,actividad, nombre_evidencia, myfile.name)
        filename = fs.save(path, myfile)
        uploaded_file_url = fs.url(filename)
        return HttpResponse('OK')
        '''return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })'''
    return render(request, 'core/simple_upload.html')


@csrf_exempt
def logout_user(request: HttpRequest): # __getattribute__('password')
    logout(request)
    return redirect('index')    # status code 302 (redirect)

def global_profile_entrepreneur(request: HttpRequest):
    # Connect to the database
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()

    # Execute an SQL command 
    data_ex = cur.execute("""SELECT (SUM(question1) + SUM(question2) + SUM(question3) + SUM(question4))  AS Autocontrol,
	    		                    (SUM(question5) + SUM(question6) + SUM(question7) + SUM(question8) + SUM(question9) + SUM(question10)) AS Leadership,
	    		                    (SUM(question11) + SUM(question12) + SUM(question13) + SUM(question14) + SUM(question15) + SUM(question16) + SUM(question17)) AS "Conscience & Social Value",
	    		                    (SUM(question18) + SUM(question19) + SUM(question20) + SUM(question21) + SUM(question22) + SUM(question23) + SUM(question24)) AS "Social Innovation & Financial Sustainability"
                             FROM app1_survey
                             GROUP BY app1_survey.num_survey;""")
    
    data = data_ex.fetchall()
    
    json_data = {'autocontrol': {'before': int(data[0][0]) if data[0][0] is not None else None,
                                  'after': int(data[1][0]) if data[1][0] is not None else None},

                 'leadership': {'before': int(data[0][1]) if data[0][1] is not None else None,
                                 'after': int(data[1][1]) if data[1][1] is not None else None},

                 'conscience_and_social_value': {'before': int(data[0][2]) if data[0][2] is not None else None,
                                                  'after': int(data[1][2]) if data[1][2] is not None else None},

                 'social_innovation_and_financial_sustainability': {'before': int(data[0][3]) if data[0][3] is not None else None,
                                                                     'after': int(data[1][3]) if data[1][3] is not None else None}}
                                                                    
    
    return HttpResponse(dumps(json_data), content_type = "application/json")
                

def global_profile_thinking(request: HttpRequest):
    # Connect to the database
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()

    # Execute an SQL command 
    data_ex = cur.execute("""SELECT  (SUM(question25) + SUM(question26) + SUM(question27) + SUM(question28)  + SUM(question29) + SUM(question30)) AS "Systemic Thinking",
				                     (SUM(question31) + SUM(question32) + SUM(question33) + SUM(question34) + SUM(question35) + SUM(question36) + SUM(question37)) AS "Scientific Thinking",
				                     (SUM(question38) + SUM(question39) + SUM(question40) + SUM(question41) + SUM(question42) + SUM(question43)) AS "Critical Thinking",
				                     (SUM(question44) + SUM(question45) + SUM(question46) + SUM(question47) + SUM(question48) + SUM(question49)) AS "Innovative Thinking"
                             FROM app1_survey
                             GROUP BY app1_survey.num_survey;""")
    
    data = data_ex.fetchall()

    json_data = {'systemic_thinking': {'before': int(data[0][0]) if data[0][0] is not None else None,
                                        'after': int(data[1][0]) if data[1][0] is not None else None},

                 'scientific_thinking': {'before': int(data[0][1]) if data[0][1] is not None else None,
                                          'after': int(data[1][1]) if data[1][1] is not None else None},

                 'critical_thinking': {'before': int(data[0][2]) if data[0][2] is not None else None,
                                        'after': int(data[1][2]) if data[1][2] is not None else None},

                 'innovative_thinking': {'before': int(data[0][3]) if data[0][3] is not None else None,
                                          'after': int(data[1][3]) if data[1][3] is not None else None}}

    return HttpResponse(dumps(json_data), content_type = "application/json")

def panel_users(request: HttpRequest):
    if (request.user.is_staff):
        return render(request, 'administracion.html')
    else:
        return render(request, 'error401.html')

def graficas(request: HttpRequest):
    return render(request, 'individual.html')

def statistics(request: HttpRequest):
    if (request.user.is_staff):
        return render(request, 'estadisticas.html')
    else:
        return render(request, 'error401.html')
    

def unique_profile_entrepreneur(request: HttpRequest, user_email: str):
    # Filtrar por email
    surveys = Survey.objects.filter(user__email=user_email, num_survey = 1)
    surveys2 = Survey.objects.filter(user__email=user_email, num_survey = 2)

    # Suma las preguntas para cada categoría
    autocontrol_b = sum([getattr(s, f'question{i}') for i in range(1, 5) for s in surveys])
    leadership_b = sum([getattr(s, f'question{i}') for i in range(5, 11) for s in surveys])
    conscience_and_social_value_b = sum([getattr(s, f'question{i}') for i in range(11, 18) for s in surveys])
    social_innovation_and_financial_sustainability_b = sum([getattr(s, f'question{i}') for i in range(18, 25) for s in surveys])

    autocontrol_a = sum([getattr(s, f'question{i}') for i in range(1, 5) for s in surveys2])
    leadership_a = sum([getattr(s, f'question{i}') for i in range(5, 11) for s in surveys2])
    conscience_and_social_value_a = sum([getattr(s, f'question{i}') for i in range(11, 18) for s in surveys2])
    social_innovation_and_financial_sustainability_a = sum([getattr(s, f'question{i}') for i in range(18, 25) for s in surveys2])

    # Preparar los datos en formato JSON
    data = {
        'autocontrol': {"before":autocontrol_b, "after":autocontrol_a},
        'leadership': {"before":leadership_b,"after":leadership_a},
        'conscience_and_social_value': {"before":conscience_and_social_value_b,"after":conscience_and_social_value_a},
        'social_innovation_and_financial_sustainability': {"before":social_innovation_and_financial_sustainability_b,"after":social_innovation_and_financial_sustainability_a}
    }

    return JsonResponse(data)


def unique_profile_thinking(request: HttpRequest, user_email: str):
    # Filtrar los resultados que coinciden con el correo dado
    results = Survey.objects.filter(user__email=user_email, num_survey = 1)
    results2 = Survey.objects.filter(user__email=user_email, num_survey = 2)

    # Sumar las respuestas de las preguntas
    systemic_thinking_b = sum([getattr(obj, f'question{i}') for i in range(25, 31) for obj in results])
    scientific_thinking_b = sum([getattr(obj, f'question{i}') for i in range(31, 38) for obj in results])
    critical_thinking_b = sum([getattr(obj, f'question{i}') for i in range(38, 44) for obj in results])
    innovative_thinking_b = sum([getattr(obj, f'question{i}') for i in range(44, 50) for obj in results])

    systemic_thinking_a = sum([getattr(obj, f'question{i}') for i in range(25, 31) for obj in results2])
    scientific_thinking_a = sum([getattr(obj, f'question{i}') for i in range(31, 38) for obj in results2])
    critical_thinking_a = sum([getattr(obj, f'question{i}') for i in range(38, 44) for obj in results2])
    innovative_thinking_a = sum([getattr(obj, f'question{i}') for i in range(44, 50) for obj in results2])

    # Crear el objeto JSON con los datos
    data = {
        'systemic_thinking': {"before":systemic_thinking_b,"after":systemic_thinking_a},
        'scientific_thinking': {"before":scientific_thinking_b,"after":scientific_thinking_a},
        'critical_thinking': {"before":critical_thinking_b,"after":critical_thinking_a},
        'innovative_thinking': {"before":innovative_thinking_b,"after":innovative_thinking_a}
    }

    # Devolver la lista como un objeto JSON
    return JsonResponse(data, safe = False)
    
def user_data(request: HttpRequest):
    users = User.objects.all().values('username', 'email', 'password')
    data = list(users)
    return JsonResponse(data, safe = False)

def pag_404_not_found(request, exception, template_name = "error404.html"):
	response = render(request, template_name)
	response.status_code = 404
	return response
