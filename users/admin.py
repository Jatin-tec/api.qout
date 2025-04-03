from django.contrib import admin
from users.models import CustomUser, UserRole

admin.site.register(CustomUser)
admin.site.register(UserRole)
