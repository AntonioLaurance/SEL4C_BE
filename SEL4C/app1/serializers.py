from django.utils import timezone
from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import *
import requests

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'second_last_name', 
                  'age', 'genre', 'country', 'institution', 'carrer', 'grade']
        

class HomeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeUser
        fields = ['username', 'password', 'name', 'first_surname', 'second_surname', 'pass_phase',
                  'email', 'created_at', 'verified_at', 'last_login', 'time_spended',
                  'rol', 'is_active', 'age', 'genre', 'country', 
                  'institution', 'carrer', 'grade']
        

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['user', 'num_survey', 'date_init', 'date_end',                                                                          # Information
                  'question1', 'question2', 'question3', 'question4',                                                       # Autocontrol 
                  'question5', 'question6', 'question7', 'question8', 'question9', 'question10',                            # Leadership
                  'question11', 'question12', 'question13', 'question14', 'question15', 'question16', 'question17',         # Conscience and social value
                  'question18', 'question19', 'question20', 'question21', 'question22', 'question23', 'question24',         # Social innovation and financial sustainability
                  'question25', 'question26', 'question27', 'question28', 'question29', 'question30',                       # Systemic thinking
                  'question31', 'question32', 'question33', 'question34', 'question35', 'question36', 'question37',         # Scientific thinking
                  'question38', 'question39', 'question40', 'question41', 'question42', 'question43',                       # Critical thinking
                  'question44', 'question45', 'question46', 'question47', 'question48', 'question49']                       # Innovative thinking


class DeliverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deliver
        fields = ['user', 'date', 'question', 'answer']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class AnswerQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerQuestion
        fields = ('id', 'user', 'question', 'answer')

    def create(self, *args, **kwargs):
        # POST to the API /respuestas
        url = "http://127.0.0.1:8000/api/respuestas/"
        
        # If we start the survey
        if(AnswerQuestion.question == 1):
            requests.post(url = url, json = {"user": AnswerQuestion.__getattribute__("user"),
                                             "date_init": timezone.now().__str__(),
                                             "date_end": "",
                                             "question1": AnswerQuestion.__getattribute__("answer"),
                                             "question2": None,
                                             "question3": None,
                                             "question4": None,
                                             "question5": None,
                                             "question6": None,
                                             "question7": None,
                                             "question8": None,
                                             "question9": None,
                                             "question10": None,
                                             "question11": None,
                                             "question12": None,
                                             "question13": None,
                                             "question14": None,
                                             "question15": None,
                                             "question16": None,
                                             "question17": None,
                                             "question18": None,
                                             "question19": None,
                                             "question20": None,
                                             "question21": None,
                                             "question22": None,
                                             "question23": None,
                                             "question24": None,
                                             "question25": None,
                                             "question26": None,
                                             "question27": None,
                                             "question28": None,
                                             "question29": None,
                                             "question30": None,
                                             "question31": None,
                                             "question32": None,
                                             "question33": None,
                                             "question34": None,
                                             "question35": None,
                                             "question36": None,
                                             "question37": None,
                                             "question38": None,
                                             "question39": None,
                                             "question40": None,
                                             "question41": None,
                                             "question42": None,
                                             "question43": None,
                                             "question44": None,
                                             "question45": None,
                                             "question46": None,
                                             "question47": None,
                                             "question48": None,
                                             "question49": None})
                                            
        # else:
        #   # Get the previus answers 
        #   elif(AnswerQuestion.question == 49):
        #       requests.put(url = url, json = {})
        #   else:
        #       requests.put(url = url, json = {})

        return super().create(*args, **kwargs)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
        