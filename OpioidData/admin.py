from django.contrib import admin
from .models import Credential, Prescriber, Drug, Triple, PrescriberCredential, Credential

# Register your models here.
admin.site.register(Prescriber)
admin.site.register(Drug)
admin.site.register(Triple)
admin.site.register(PrescriberCredential)
admin.site.register(Credential)