from django.contrib.auth.models import AbstractUser 
from django.utils import timezone
from django.db import models
from datetime import timedelta

# Create your models here.
class User(AbstractUser):
    # Login information
    email = models.EmailField('email address', primary_key = True, null = False, unique = True)
    second_last_name = models.CharField(max_length = 150, null = False, default = "")
    pass_phase = models.CharField(max_length = 255, null = True, blank = False)

    # User Information
    time_spended = models.DurationField(default = timedelta(days = 0, hours = 0, minutes = 0, seconds = 0))
    verified_at = models.DateTimeField(null = True)

    # Data analysis    
    age = models.PositiveSmallIntegerField(null = True)
    genre = models.CharField(max_length = 255, null = True)
    country = models.CharField(max_length = 255, null = True)      
    institution = models.CharField(max_length = 255, null = True)
    carrer = models.CharField(max_length = 255, null = True)
    grade = models.CharField(max_length = 255, null = True)

    # Change the attribute for the login for the user
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        swappable = 'AUTH_USER_MODEL'


class HomeUser(models.Model):
    # Login Information
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    pass_phase = models.CharField(max_length = 255)
    
    # User Information
    name = models.CharField(max_length = 255, null = False, default = "Anónimo")
    first_surname = models.CharField(max_length = 255, null = True)
    second_surname = models.CharField(max_length = 255, null = True)
    email = models.EmailField(null = False)
    created_at = models.DateTimeField(default = timezone.now)
    last_login = models.DateTimeField(null = True)
    time_spended = models.DurationField(default = timedelta(days = 0, hours = 0, minutes = 0, seconds = 0))
    rol = models.CharField(max_length = 15, choices = (("U", "Usuario"), 
                                                       ("A", "Administrador")), default = "Usuario")
    verified_at = models.DateTimeField(null = True)
    is_active = models.BooleanField(null = False, blank = False, default = True)

    # Data analysis    
    age = models.PositiveSmallIntegerField(null = False)
    genre = models.CharField(max_length = 255, null = False)
    country = models.CharField(max_length = 255, null = False)      
    institution = models.CharField(max_length = 255, null = True)
    carrer = models.CharField(max_length = 15, null = True)

    grade = models.CharField(max_length = 10, null = True)
    
    
    def __str__(self):
        return f"{self.name} {self.first_surname} {self.second_surname}"
    
    class Meta:
        app_label = "app1"


class Session(models.Model):
    # Identification
    user = models.ForeignKey(User, null = False, blank = False, on_delete = models.CASCADE)
    ip_address = models.GenericIPAddressField(null = True, blank = False)

    # Duration
    date_init = models.DateTimeField(null = False, blank = False)
    date_end = models.DateTimeField(null = False, blank = False)

    def __str__(self):
        return f"{self.user} con dirección IP: {self.ip_address}"

    class Meta:
        app_label = "app1"


class Survey(models.Model):
    user = models.ForeignKey(User, null = False, blank = False, on_delete = models.CASCADE)
    date_init = models.DateTimeField(null = False, blank = False)
    date_end = models.DateTimeField(null = False, blank = False)

    # -----------------------------------------------------------------------------------------------
    # Social Entrepreneur Profile
    # -----------------------------------------------------------------------------------------------

    # Autocontrol 
    question1 = models.PositiveSmallIntegerField(null = True, blank = False)    # Motivation
    question2 = models.PositiveSmallIntegerField(null = True, blank = False)    # Perseverance and resilience
    question3 = models.PositiveSmallIntegerField(null = True, blank = False)    # Perseverance and resilience
    question4 = models.PositiveSmallIntegerField(null = True, blank = False)    # Tolerance to uncertainty, ambiguity and mastery of stress

    # Leadership
    question5 = models.PositiveSmallIntegerField(null = True, blank = False)    # Strategic planning
    question6 = models.PositiveSmallIntegerField(null = True, blank = False)    # Communication and persuasion
    question7 = models.PositiveSmallIntegerField(null = True, blank = False)    # Communication and persuasion
    question8 = models.PositiveSmallIntegerField(null = True, blank = False)    # Mobilize people
    question9 = models.PositiveSmallIntegerField(null = True, blank = False)    # Mobilize people
    question10 = models.PositiveSmallIntegerField(null = True, blank = False)   # Collaborative working

    # Conscience and social value
    question11 = models.PositiveSmallIntegerField(null = True, blank = False)   # Social implication
    question12 = models.PositiveSmallIntegerField(null = True, blank = False)   # Social implication
    question13 = models.PositiveSmallIntegerField(null = True, blank = False)   # Empathy
    question14 = models.PositiveSmallIntegerField(null = True, blank = False)   # Identification of social/environmental problems
    question15 = models.PositiveSmallIntegerField(null = True, blank = False)   # Identification of social/environmental problems
    question16 = models.PositiveSmallIntegerField(null = True, blank = False)   # Sustainability orientation
    question17 = models.PositiveSmallIntegerField(null = True, blank = False)   # Ethical sense

    # Social innovation and financial sustainability
    question18 = models.PositiveSmallIntegerField(null = True, blank = False)   # Creativity
    question19 = models.PositiveSmallIntegerField(null = True, blank = False)   # Economic and financial literacy
    question20 = models.PositiveSmallIntegerField(null = True, blank = False)   # Economic and financial literacy
    question21 = models.PositiveSmallIntegerField(null = True, blank = False)   # Economic and financial literacy
    question22 = models.PositiveSmallIntegerField(null = True, blank = False)   # Valuation of ideas, results and impacts on the environment and people
    question23 = models.PositiveSmallIntegerField(null = True, blank = False)   # Learning and adaptability
    question24 = models.PositiveSmallIntegerField(null = True, blank = False)   # Management of limited resources for social projects

    # -----------------------------------------------------------------------------------------------
    # Complex Thinking 
    # -----------------------------------------------------------------------------------------------

    # Systemic thinking
    question25 = models.PositiveSmallIntegerField(null = True, blank = False)   # Knowledge
    question26 = models.PositiveSmallIntegerField(null = True, blank = False)   # Knowledge
    question27 = models.PositiveSmallIntegerField(null = True, blank = False)   # Skills
    question28 = models.PositiveSmallIntegerField(null = True, blank = False)   # Skills
    question29 = models.PositiveSmallIntegerField(null = True, blank = False)   # Attitudes and values
    question30 = models.PositiveSmallIntegerField(null = True, blank = False)   # Attitudes and values

    # Scientific thinking
    question31 = models.PositiveSmallIntegerField(null = True, blank = False)   # Knowledge
    question32 = models.PositiveSmallIntegerField(null = True, blank = False)   # Knowledge
    question33 = models.PositiveSmallIntegerField(null = True, blank = False)   # Knowledge
    question34 = models.PositiveSmallIntegerField(null = True, blank = False)   # Skills
    question35 = models.PositiveSmallIntegerField(null = True, blank = False)   # Skills
    question36 = models.PositiveSmallIntegerField(null = True, blank = False)   # Skills
    question37 = models.PositiveSmallIntegerField(null = True, blank = False)   # Attitudes and values

    # Critical thinking
    question38 = models.PositiveSmallIntegerField(null = True, blank = False)   # Knowledge
    question39 = models.PositiveSmallIntegerField(null = True, blank = False)   # Knowledge
    question40 = models.PositiveSmallIntegerField(null = True, blank = False)   # Skills
    question41 = models.PositiveSmallIntegerField(null = True, blank = False)   # Skills
    question42 = models.PositiveSmallIntegerField(null = True, blank = False)   # Attitudes and values
    question43 = models.PositiveSmallIntegerField(null = True, blank = False)   # Attitudes and values

    # Innovative thinking
    question44 = models.PositiveSmallIntegerField(null = True, blank = False)   # Knowledge
    question45 = models.PositiveSmallIntegerField(null = True, blank = False)   # Knowledge
    question46 = models.PositiveSmallIntegerField(null = True, blank = False)   # Skills
    question47 = models.PositiveSmallIntegerField(null = True, blank = False)   # Skills
    question48 = models.PositiveSmallIntegerField(null = True, blank = False)   # Skills
    question49 = models.PositiveSmallIntegerField(null = True, blank = False)   # Attitudes and values

    class Meta:
        app_label = "app1"


class Deliver(models.Model):
    user = models.ForeignKey(User, null = False, blank = False, on_delete = models.CASCADE) # ¿Qué desaparezcan las entregas de un usuario cuando lo eliminamos inmediatamente?
    date = models.DateTimeField(null = False, blank = False)

    # Types of files that an user can deliver
    text_file = models.TextField(null = True, blank = True)
    image_file = models.ImageField(null = True, blank = True)
    url_file = models.URLField(null = True, blank = True)
    file = models.FileField(null = True, blank = True)

    class Meta:
        app_label = "app1"
