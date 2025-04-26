from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

admin.site.register(User, CustomUserAdmin)
