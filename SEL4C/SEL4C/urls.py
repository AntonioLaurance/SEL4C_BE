"""
URL configuration for SEL4C project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import handler404
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView
from rest_framework import routers
from app1 import views

router = routers.DefaultRouter()
router.register(r'usuarios', views.UserViewSet)
router.register(r'sesiones', views.SessionViewSet)
router.register(r'preguntas', views.QuestionViewSet)
router.register(r'respuestas', views.SurveyViewSet)
router.register(r'respuestas_detalladas', views.AnswerQuestionViewSet)
router.register(r'entregas', views.DeliverViewSet)

# Our customized 404 error page
handler404 = views.pag_404_not_found

# Wire op our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API. 
urlpatterns = [
    path('', views.index, name = 'index'),
    path('contacto/', views.contacto, name = 'contacto'),
    path('registro/', views.register, name = 'registro'),
    path('graficas/', views.graficas, name = 'graficas'),
    path('usuarios/', views.panel_users, name = 'usuarios'),
    path('estadisticas/', views.statistics, name = 'estadisticas'),
    path('login/', views.LoginView.as_view(template_name = 'iniciosesion.html'), name = 'login'),
    path('auth/', views.auth, name = 'auth'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace = 'rest_framework')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/user_data/', views.user_data, name='user_data'),
    path('api/graph-social/', views.global_profile_entrepreneur, name = 'graph social'),
    path('api/graph-thinking/', views.global_profile_thinking, name = 'graph thinking'),
    path('api/unique-graph-social/<str:user_email>/', views.unique_profile_entrepreneur, name='profile_entrepreneur'),
    path('api/unique-graph-thinking/<str:user_email>/', views.unique_profile_thinking, name='profile_thinking'),
    path('user_responses/', views.user_responses, name='user_responses'),
    path('UploadFile', views.UploadFile, name='UploadFile'),
    path('simple_upload', views.simple_upload, name='simple_upload'),
    path('logout/', views.logout_user, name = 'logout')
]

