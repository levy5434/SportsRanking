"""Stores urls"""

from api import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"league", views.LeagueViewSet, basename="league")
router.register(r"team", views.TeamViewSet, basename="team")
router.register(r"match", views.MatchViewSet, basename="match")
router.register(r"matchday", views.MatchdayViewSet, basename="matchday")
router.register(r"myleague", views.MyLeagueViewSet, basename="myleague")
router.register(
    r"predictions", views.PredictionViewSet, basename="predictions"
)

app_name = "api"

urlpatterns = [
    path("", include(router.urls)),
    path(
        "addplayer/<str:myLeagueId>",
        views.MyLeagueAddPlayerView.as_view(),
        name="add_player",
    ),
]
