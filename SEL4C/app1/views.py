from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import viewsets
from rest_framework import permissions
from app1.models import User, HomeUser, Session, Survey, Deliver
from app1.serializers import UserSerializer, HomeUserSerializer, SessionSerializer, SurveySerializer, DeliverSerializer, GroupSerializer
from json import loads, dumps

# Create your views here.
# @csrf_exempt
# def login(request):
#    return render(request, LoginView.as_view(template_name = 'iniciosesion.html'))

# Authentificate users in external sites
# This functions with the HTTP verb 'POST'
@csrf_exempt
def auth(request):
    # Deserialization
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)
 
    # Authentification with given credentials
    # login(request, )
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
