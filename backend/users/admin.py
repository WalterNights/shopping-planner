from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')
        
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = User
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
                'fields': (
                    'username', 
                    'email', 
                    'password1', 
                    'password2', 
                    'rol', 
                    'is_staff', 
                    'is_active'
                )
            }
        ),
    )
    list_display = ('username', 'email', 'rol', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    
admin.site.register(User, CustomUserAdmin)