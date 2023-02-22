from django.contrib import admin

from . import models

admin.site.register(models.ReferenceBook)
admin.site.register(models.ReferenceBookVersion)
admin.site.register(models.ReferenceBookElement)
# todo дополнить админку требованиями тз
