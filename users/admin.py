from django.contrib import admin
from users.models import CustomUser, UserRole

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ( 'email', 'first_name', 'last_name', 'is_staff', 'role')
    list_filter = ('is_staff', 'is_active', 'role')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserRole)
