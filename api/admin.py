from django.contrib import admin
from . import models


admin.site.register(models.Team)
admin.site.register(models.Position)
admin.site.register(models.SynchronUser)
admin.site.register(models.SyncupBoard)
admin.site.register(models.StandupCard)
admin.site.register(models.IndividualCardUpdate)