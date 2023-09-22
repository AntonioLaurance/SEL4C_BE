from django.contrib import admin
from .models import User
from app1.models import Session, Survey, Deliver

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # fields = ('username', 'password', 'first_name', 'last_name', 'second_last_name', 'email', 'pass_phase')
    fieldsets = (
        (None, {
            'fields': ('username', 'pass_phase', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 
                       'second_last_name', 'email', 
                       'age', 'genre', 'country')
        }), 
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions')
        }), 
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }), 
        ('Academic info', {
            'fields': ('institution', 'carrer', 'grade')
        })
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'second_last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    pass

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    pass

@admin.register(Deliver)
class DeliverAdmin(admin.ModelAdmin):
    pass

# Update app name
name = "SEL4C.app1"