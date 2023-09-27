from django.shortcuts import render
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from .models import User
from rest_framework import viewsets
from rest_framework import permissions
from app1.models import HomeUser, Session, Survey, Deliver
from app1.serializers import UserSerializer, HomeUserSerializer, SessionSerializer, SurveySerializer, DeliverSerializer, GroupSerializer

# Create your views here.
@csrf_exempt
def login(request):
    return render(request, LoginView.as_view(template_name = 'iniciosesion.html'))


class DangerousLoginView(LoginView):
    '''A LoginView with no CSRF protection.'''

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            return HttpResponseRedirect(redirect_to)
        return super(LoginView, self).dispatch(request, *args, **kwargs)

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
