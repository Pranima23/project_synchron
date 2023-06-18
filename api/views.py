from .models import *
from rest_framework import viewsets, generics
from .serializers import *
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import IsSMorReadOnlyPermissions
from datetime import date, timedelta
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import connection


def filter_standup_cards_by_user(user):
    user_team = user.synchron_user.team.id
    return StandupCard.objects.raw(
            'SELECT * FROM api_standupcard WHERE team_id = %s', [user_team]
            )

def filter_standup_cards_by_date(date):
    return StandupCard.objects.raw(
            'SELECT * FROM api_standupcard WHERE standup_date = %s', [date]
            )

def filter_standup_cards_by_user_and_date(user, date):
    user_team = user.synchron_user.team.id
    return StandupCard.objects.raw(
            """SELECT * FROM api_standupcard 
            WHERE team_id = %s 
            AND standup_date = %s""", [user_team, date]
            )


class StandupCardViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing standup card instances
    """
    def get_queryset(self):
        """ Filters standup cards according to team of user """
        queryset = StandupCard.objects.raw(
            'SELECT * FROM api_standupcard'
            )
        
        if not self.request.user.is_superuser:
            queryset = filter_standup_cards_by_user(self.request.user)

        return queryset
    
    serializer_class = StandupCardSerializer
    permission_classes = [IsSMorReadOnlyPermissions, IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    
class StandupCardByDateView(generics.ListAPIView):
    """
    A viewset for viewing standup card instances by date
    """
    def get_queryset(self):
        """ Filters standup cards according to query date and team of user """
        date = self.kwargs["date"]

        queryset = filter_standup_cards_by_date(date)        
        if not self.request.user.is_superuser:
            queryset = filter_standup_cards_by_user_and_date(self.request.user, date)

        return queryset
        
    serializer_class = StandupCardSerializer


class StanupCardTodayView(generics.ListAPIView):
    """
    A viewset for viewing today's standup card instances
    """
    def get_queryset(self):
        """ Filters standup cards for present day according to date and team of user """
        date = date.today()

        queryset = filter_standup_cards_by_date(date)        
        if not self.request.user.is_superuser:
            queryset = filter_standup_cards_by_user_and_date(self.request.user, date)

        return queryset
        
    serializer_class = StandupCardSerializer


class StanupCardYesterdayView(generics.ListAPIView):
    """
    A viewset for viewing yesterday's standup card instances
    """
    def get_queryset(self):
        """ Filters standup cards for the last day according to date and team of user """
        date = date.today() - timedelta(1)

        queryset = filter_standup_cards_by_date(date)        
        if not self.request.user.is_superuser:
            queryset = filter_standup_cards_by_user_and_date(self.request.user, date)

        return queryset
        
    serializer_class = StandupCardSerializer


class StandupCardByMonthView(generics.ListAPIView):
    """
    A viewset for viewing standup card instances by month
    """
    def get_queryset(self):
        """ Filters standup cards according to queried month of year and team of user """
        year = self.kwargs['year']
        month = self.kwargs['month']

        queryset = StandupCard.objects.raw(
            """SELECT * FROM api_standupcard 
            WHERE date_part('year', standup_date) = %s
            AND date_part('month', standup_date) = %s""", 
            [year, month]             
            )
        
        if not self.request.user.is_superuser:
            user_team = self.request.user.synchron_user.team.id
            queryset = StandupCard.objects.raw(
            """SELECT * FROM api_standupcard 
            WHERE date_part('year', standup_date) = %s
            AND date_part('month', standup_date) = %s
            AND team_id = %s""", 
            [year, month, user_team]             
            )

        return queryset
        
    serializer_class = StandupCardSerializer
    

class StandupCardBySprintIDView(generics.ListAPIView):
    """
    A viewset for viewing standup card instances by sprint ID
    """
    def get_queryset(self):
        """ Filters standup cards according to query sprint ID and team of user """
        sprint_id = self.kwargs['sprint_id']

        queryset = StandupCard.objects.raw(
            'SELECT * FROM api_standupcard WHERE sprint_id = %s', [sprint_id]             
            )
        
        if not self.request.user.is_superuser:
            user_team = self.request.user.synchron_user.team.id
            queryset = StandupCard.objects.raw(
            """SELECT * FROM api_standupcard 
            WHERE sprint_id = %s
            AND team_id = %s""", 
            [sprint_id, user_team]             
            )

        return queryset
        
    serializer_class = StandupCardSerializer


# def standup_cards_this_month(request):
#     if request.method == 'GET':
#         todays_date = date.today()
#         current_year = todays_date.year
#         current_month = todays_date.month
#         standup_cards = StandupCard.objects.filter(standup_date__year=current_year, standup_date__month=current_month)
#         serializer = StandupCardSerializer(standup_cards, many=True)
#         return JsonResponse(serializer.data, safe=False)
    

# class PositionViewSet(viewsets.ModelViewSet):
#     """
#     A viewset for viewing and editing position instances
#     """
#     queryset = Position.objects.all()
#     serializer_class = PositionSerializer
#     # authentication_classes = [TokenAuthentication]  # Add the desired authentication class
#     permission_classes = [IsSMorReadOnlyPermissions]


# class TeamViewSet(viewsets.ModelViewSet):
#     """
#     A viewset for viewing and editing team instances
#     """
#     queryset = Team.objects.all()
#     serializer_class = TeamSerializer
    # permission_classes = [AdminPermissions]


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     A viewset for viewing and editing group instances
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [AdminPermissions]


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     A viewset for viewing and editing user instances
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     # lookup_field = 'pk'
#     permission_classes = [AdminPermissions]


# class SynchronUserViewSet(viewsets.ModelViewSet):
#     """
#     A viewset for viewing and editing synchron user instances
#     """
#     queryset = SynchronUser.objects.all()
#     serializer_class = SynchronUserSerializer
#     permission_classes = [AdminPermissions]


# class SyncupBoardViewSet(viewsets.ModelViewSet):
#     """
#     A viewset for viewing and editing syncup board instances
#     """
#     queryset = SyncupBoard.objects.all()
#     serializer_class = SyncupBoardSerializer
#     permission_classes = [IsSMorReadOnlyPermissions]

# class IndividualCardUpdateViewSet(viewsets.ModelViewSet):
#     """
#     A viewset for viewing and editing individual card update instances
#     """
#     queryset = IndividualCardUpdate.objects.all()
#     serializer_class = IndividualCardUpdateSerializer
#     permission_classes = [IsSMorReadOnlyPermissions]