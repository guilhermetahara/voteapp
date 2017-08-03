from django.contrib import admin
from . import models

admin.site.register(models.Votacao)
admin.site.register(models.Escolha)
admin.site.register(models.Voto)

