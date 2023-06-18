from django.contrib import admin
from . import models


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'team_name', 'scrum_master')


@admin.register(models.SynchronUser)
class SynchronuserAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'position')


@admin.register(models.StandupCard)
class StandupCardAdmin(admin.ModelAdmin):
    list_display = ('team', 'scrum_master', 'release_cycle', 'sprint_id')


admin.site.register(models.Position)
admin.site.register(models.IndividualCardUpdate)