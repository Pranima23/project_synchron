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


class StandupCardViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing standup card instances
    """
    def get_queryset(self):
        """ Filters standup cards according to team of user """
        queryset = StandupCard.objects.all()
        if self.request.user.is_superuser:
            return queryset
        user_team = self.request.user.synchron_user.team
        queryset = StandupCard.objects.filter(team=user_team)
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
        queryset = StandupCard.objects.filter(standup_date=self.kwargs["date"])
        if self.request.user.is_superuser:
            return queryset
        user_team = self.request.user.synchron_user.team
        queryset = queryset.filter(team=user_team)
        return queryset
        
    serializer_class = StandupCardSerializer


class StanupCardTodayView(generics.ListAPIView):
    """
    A viewset for viewing today's standup card instances
    """
    def get_queryset(self):
        """ Filters standup cards for present day according to date and team of user """
        queryset = StandupCard.objects.filter(standup_date=date.today())
        if self.request.user.is_superuser:
            return queryset
        user_team = self.request.user.synchron_user.team
        queryset = queryset.filter(team=user_team)
        return queryset
        
    serializer_class = StandupCardSerializer


class StanupCardYesterdayView(generics.ListAPIView):
    """
    A viewset for viewing yesterday's standup card instances
    """
    def get_queryset(self):
        """ Filters standup cards for the last day according to date and team of user """
        yesterday = date.today() - timedelta(1)
        queryset = StandupCard.objects.filter(standup_date=yesterday)
        if self.request.user.is_superuser:
            return queryset
        user_team = self.request.user.synchron_user.team
        queryset = queryset.filter(team=user_team)
        return queryset
        
    serializer_class = StandupCardSerializer


class StandupCardByMonthView(generics.ListAPIView):
    """
    A viewset for viewing standup card instances by month
    """
    def get_queryset(self):
        """ Filters standup cards according to queried month of year and team of user """
        queryset = StandupCard.objects.filter(standup_date__year=self.kwargs['year'], standup_date__month=self.kwargs['month'])
        if self.request.user.is_superuser:
            return queryset
        user_team = self.request.user.synchron_user.team
        queryset = queryset.filter(team=user_team)
        return queryset
        
    serializer_class = StandupCardSerializer
    

class StandupCardBySprintIDView(generics.ListAPIView):
    """
    A viewset for viewing standup card instances by sprint ID
    """
    def get_queryset(self):
        """ Filters standup cards according to query sprint ID and team of user """
        queryset = StandupCard.objects.filter(sprint_id=self.kwargs['sprint_id'])
        if self.request.user.is_superuser:
            return queryset
        user_team = self.request.user.synchron_user.team
        queryset = queryset.filter(team=user_team)
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