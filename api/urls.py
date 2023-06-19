from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
# router.register(r'positions', views.PositionViewSet, basename="position")
# router.register(r'teams', views.TeamViewSet, basename="team")
# router.register(r'groups', views.GroupViewSet, basename="group")
# router.register(r'users', views.UserViewSet, basename="user")
# router.register(r'synchronusers/', views.SynchronUserViewSet, basename="synchronuser")
router.register(r'standupcard', views.StandupCardViewSet, basename="standupcard")
# router.register(r'updates', views.IndividualCardUpdateViewSet, basename="individualcardupdate")


urlpatterns = [
    path(route='standupcard/by_date/<str:date>/', view=views.StandupCardByDateView.as_view()),
    path(route='standupcard/today/', view=views.StandupCardTodayView.as_view()),
    path(route='standupcard/yesterday/', view=views.StandupCardYesterdayView.as_view()),
    path(route='standupcard/by_month/<int:year>/<int:month>/', view=views.StandupCardByMonthView.as_view()),
    path(route='standupcard/by_sprint_id/<str:sprint_id>/', view=views.StandupCardBySprintIDView.as_view()),
    path(route='', view=include(router.urls)),
]