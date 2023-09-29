from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from app1.models import User, HomeUser, Session, Survey, Deliver
from app1.serializers import UserSerializer, HomeUserSerializer, SessionSerializer, SurveySerializer, DeliverSerializer, GroupSerializer
from rest_framework import viewsets, permissions
from json import loads, dumps
import sqlite3

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
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('date_joined')
    serializer_class = UserSerializer

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

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

# Home page    
def index(request):
    return render(request, 'index.html')

# Contact page
def contacto(request):
    return render(request, 'contacto.html')

@csrf_exempt
def logout_user(request):
    logout(request)
    return redirect('login')

def global_profile_entrepreneur(request: HttpRequest):
    # Connect to the database
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()

    # Execute an SQL command 
    data_ex = cur.execute("""SELECT (SUM(question1) + SUM(question2) + SUM(question3) + SUM(question4))  AS Autocontrol,
	    		       	            (SUM(question5) + SUM(question6) + SUM(question7) + SUM(question8) + SUM(question9) + SUM(question10)) AS Leadership,
	    		       	            (SUM(question11) + SUM(question12) + SUM(question13) + SUM(question14) + SUM(question15) + SUM(question16) + SUM(question17)) AS "Conscience & Social Value",
	    		       	            (SUM(question18) + SUM(question19) + SUM(question20) + SUM(question21) + SUM(question22) + SUM(question23) + SUM(question24)) AS "Social Innovation & Financial Sustainability"
                             FROM app1_survey;""")
    
    data = data_ex.fetchall()
    
    json_data = {'autocontrol': int(data[0][0]) if data[0][0] is not None else None,
                 'leadership': int(data[0][1]) if data[0][1] is not None else None,
                 'conscience_and_social_value': int(data[0][2]) if data[0][2] is not None else None,
                 'social_innovation_and_financial_sustainability': int(data[0][3]) if data[0][3] is not None else None}
    
    return HttpResponse(dumps(json_data), content_type = "application/json")
                

def global_profile_thinking(request: HttpRequest):
    pass
