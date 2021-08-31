from django.contrib import admin
from .models import CustomUser,ActivationLinks

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(ActivationLinks)


