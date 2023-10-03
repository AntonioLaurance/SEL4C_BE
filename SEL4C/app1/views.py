from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse
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
 
    # Authentification with given credentials
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
    permission_classes = [permissions.IsAdminUser]

class DeliverViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Deliver.objects.all()
    serializer_class = DeliverSerializer
    permission_classes = [permissions.IsAdminUser]

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

@csrf_exempt
def UploadFile(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print(form.fields['author'])
            return HttpResponse('The file is saved')
    else:
        form = BlogForm()
    context = {'form': form,}
    return render(request, 'upload.html', context)

@csrf_exempt
def simple_upload(request):
    if request.method == 'POST' and request.FILES['file']:
        usuario =(request.POST['user'])
        actividad=(request.POST['activity'])
        nombre_evidencia=(request.POST['evidence_name'])
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
def logout_user(request):
    logout(request)
    return redirect('admin')

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
        return HttpResponse("<h1>Panel de usuarios</h1>Acceso no autorizado")

def graficas(request: HttpRequest):
    return render(request, 'graficas.html')
