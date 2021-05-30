"""Stores ViewSets."""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import League, Team, Matchday, Match, MyLeague, Prediction
from rest_framework import viewsets
from api.serializers import (
    LeagueSerializer,
    TeamSerializer,
    MatchSerializer,
    MatchdaySerializer,
    MyLeagueSerializer,
    PredictionSerializer,
)
from rest_framework.permissions import IsAuthenticated


class LeagueViewSet(viewsets.ModelViewSet):
    """ViewSet for class League."""

    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    lookup_field = "leagueCode"


class TeamViewSet(viewsets.ModelViewSet):
    """ViewSet for class Team."""

    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class MatchdayViewSet(viewsets.ModelViewSet):
    """ViewSet for class Matchday."""

    # permission_classes = [IsAuthenticated]
    serializer_class = MatchdaySerializer
    lookup_field = "leagueCode"
    queryset = Matchday.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("leagueCode", "number")


class MatchViewSet(viewsets.ModelViewSet):
    """ViewSet for class Match."""

    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class MyLeagueViewSet(viewsets.ModelViewSet):
    """ViewSet for class MyLeague."""

    permission_classes = [IsAuthenticated]
    serializer_class = MyLeagueSerializer

    def get_queryset(self):
        user = self.request.user
        return MyLeague.objects.filter(players=user)


class MyLeagueAddPlayerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, myLeagueId):
        try:
            myLeague = MyLeague.objects.get(myLeagueId=myLeagueId)
            user = self.request.user
            myLeague.players.add(user)
            return Response(
                {"Success": "You joined new MyLeague!"},
                status=status.HTTP_202_ACCEPTED,
            )
        except:  # noqa
            return Response(
                {"Failed": "MyLeague with this id doesn't exist!"},
                status=status.HTTP_HTTP_400_BAD_REQUEST,
            )


class PredictionViewSet(viewsets.ModelViewSet):
    """ViewSet for class Prediction."""

    permission_classes = [IsAuthenticated]
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer
