from django.contrib import admin
from .models import Prescriber, Drug, Triple

# Register your models here.
admin.site.register(Prescriber)
admin.site.register(Drug)
admin.site.register(Triple)