from django.db import models
from django.contrib.auth.models import User, Group


class Team(models.Model):
    team_name = models.CharField(max_length=50)

    def __str__(self):
        return self.team_name


class Position(models.Model):
    position_name = models.CharField(max_length=50)

    def __str__(self):
        return self.position_name


class SynchronUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    full_name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.full_name


class SyncupBoard(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.team


class StandupCard(models.Model):
    syncup = models.ForeignKey(SyncupBoard, on_delete=models.CASCADE)
    standup_date = models.DateField(auto_now_add=True)
    release_cycle = models.CharField(max_length=255)
    sprint_id = models.IntegerField()
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Release cycle{self.release_cycle}, Sprint ID {self.sprint_id}"
    

class IndividualCardUpdate(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    standup_card = models.ForeignKey(StandupCard, on_delete=models.CASCADE)
    member = models.ForeignKey(SynchronUser, on_delete=models.SET_NULL, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)