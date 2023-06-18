from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    """
    A model to store teams in organization
    """
    team_name = models.CharField(max_length=50)

    @property
    def scrum_master(self):
        members = self.team_members.all()
        for member in members:
             if member.user.groups.filter(name='Scrum Master').exists():
                return member

    def __str__(self):
        return self.team_name


class Position(models.Model):
    """
    A model to store positions of organization members
    """
    position_name = models.CharField(max_length=50)

    def __str__(self):
        return self.position_name


class SynchronUser(models.Model):
    """
    A model to store information about organization members
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='synchron_user')
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='team_members')
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True, related_name='synchron_users')

    def __str__(self):
        return f"{self.user.username}"


class StandupCard(models.Model):
    """
    A model to store standup cards
    """
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='standup_cards')
    standup_date = models.DateField(auto_now_add=True)
    release_cycle = models.CharField(max_length=255)
    sprint_id = models.IntegerField()
    notes = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['team', 'release_cycle', 'sprint_id'], name = 'standup_card_constraint'),
            ]
        
    @property
    def scrum_master(self):
        return self.team.scrum_master

    def __str__(self):
        return f"{self.team} Release Cycle {self.release_cycle}, Sprint ID {self.sprint_id}"
    

class IndividualCardUpdate(models.Model):
    """
    A model to store individual member remarks in a standup card
    """
    updated_at = models.DateTimeField(auto_now=True)
    standup_card = models.ForeignKey(StandupCard, on_delete=models.CASCADE, related_name='individual_updates')
    member = models.ForeignKey(SynchronUser, on_delete=models.SET_NULL, related_name='individual_updates', null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.member.user.username} {self.remarks}"