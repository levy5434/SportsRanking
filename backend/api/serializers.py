from rest_framework import serializers
from api.sportsapi import LeagueApi, MatchdayApi
from api.models import Team, League, Match, Matchday, MyLeague, Prediction
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            "teamId",
            "name",
            "league",
            "form",
            "playedGames",
            "position",
            "won",
            "draw",
            "lost",
            "points",
            "goalsScored",
            "goalsAgainst",
            "goalDifference",
        ]

        read_only_fields = (
            "teamId",
            "name",
            "league",
            "form",
            "playedGames",
            "position",
            "won",
            "draw",
            "lost",
            "points",
            "goalsScored",
            "goalsAgainst",
            "goalDifference",
        )


class LeagueSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(many=True, read_only=True)

    class Meta:
        model = League
        fields = ["leagueCode", "name", "teams", "logo"]

        extra_kwargs = {
            "name": {"read_only": True},
            "logo": {"read_only": True},
        }

    def create(self, validated_data):
        if not self.is_valid():
            return None
        teams = LeagueApi(self.validated_data["leagueCode"])
        resp = teams.make_request()
        leagueName = teams.leagueName
        league = League(
            leagueCode=self.validated_data["leagueCode"], name=leagueName
        )
        league.save()
        teams = teams.get_teams(resp)
        for team in teams:
            new_team = Team(
                teamId=team["teamId"],
                name=team["name"],
                logo=team["logo"],
                league=league,
                position=team["position"],
                form=team["form"],
                playedGames=team["playedGames"],
                won=team["won"],
                draw=team["draw"],
                lost=team["lost"],
                points=team["points"],
                goalsScored=team["goalsScored"],
                goalsAgainst=team["goalsAgainst"],
                goalDifference=team["goalDifference"],
            )
            new_team.save()
        return league


class MatchSerializer(serializers.ModelSerializer):
    homeTeamName = serializers.StringRelatedField(
        source="homeTeam", read_only=True
    )
    awayTeamName = serializers.StringRelatedField(
        source="awayTeam", read_only=True
    )
    leagueName = serializers.StringRelatedField(
        source="league", read_only=True
    )
    matchdayNumber = serializers.StringRelatedField(
        source="matchday", read_only=True
    )

    class Meta:
        model = Match
        fields = (
            "matchId",
            "leagueName",
            "matchdayNumber",
            "homeTeamName",
            "awayTeamName",
            "date",
            "time",
            "result",
            "status",
            "homeTeamScore",
            "awayTeamScore",
        )
        read_only_fields = (
            "matchId",
            "date",
            "time",
            "result",
            "status",
            "homeTeamScore",
            "awayTeamScore",
        )


class MatchdaySerializer(serializers.ModelSerializer):
    matches = MatchSerializer(many=True, read_only=True)

    class Meta:
        model = Matchday
        fields = ["leagueCode", "number", "matches"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["leagueCode"] = LeagueSerializer(instance.leagueCode).data[
            "leagueCode"
        ]
        return rep

    def create(self, validated_data):
        if not self.is_valid():
            return None
        matches = MatchdayApi(
            self.validated_data["leagueCode"].leagueCode,
            self.validated_data["number"],
        )
        resp = matches.make_request()
        matches = matches.get_matches(resp)
        league = League.objects.get(
            leagueCode=self.validated_data["leagueCode"].leagueCode
        )
        matchday = Matchday(
            leagueCode=league, number=self.validated_data["number"]
        )
        matchday.save()
        for match in matches:
            homeTeam = Team.objects.get(teamId=match["homeTeam"])
            awayTeam = Team.objects.get(teamId=match["awayTeam"])
            if match["winner"] == "HOME_TEAM":
                result = homeTeam.name
            elif match["winner"] == "AWAY_TEAM":
                result = awayTeam.name
            else:
                result = match["winner"]
            new_match = Match(
                matchId=match["matchId"],
                homeTeam=homeTeam,
                awayTeam=awayTeam,
                league=league,
                date=match["date"],
                time=match["time"],
                result=result,
                homeTeamScore=match["homeTeamScore"],
                awayTeamScore=match["awayTeamScore"],
                status=match["status"],
                matchday=matchday,
            )
            new_match.save()
        return matchday


class MyLeagueSerializer(serializers.ModelSerializer):
    leagueCodes = serializers.ListField(source="get_league_codes")

    class Meta:
        model = MyLeague
        fields = ["name", "myLeagueId", "leagueCodes", "players"]
        read_only_fields = ("myLeagueId", "players")

    def create(self, validated_data):
        if not self.is_valid():
            return None
        myLeague = MyLeague(
            name=self.validated_data["name"],
            myLeagueId=get_random_string(8).lower(),
        )
        myLeague.save()
        user_id = self.context["request"].user.id
        owner = User.objects.get(id=user_id)
        myLeague.players.add(owner)
        for leagueCode in self.validated_data["get_league_codes"]:
            league = League.objects.get(leagueCode=leagueCode)
            myLeague.leagues.add(league)
        return myLeague


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = ["player", "match", "prediction", "points", "myLeague"]

        read_only_fields = ("points",)

    def create(self, validated_data):
        if not self.is_valid or self.validated_data["match"].result:
            raise serializers.ValidationError("Prediction is over!")
        prediction = Prediction(
            match=self.validated_data["match"],
            prediction=self.validated_data["prediction"],
            myLeague=self.validated_data["myLeague"],
        )
        if self.validated_data["match"].result == prediction.prediction:
            prediction.points = 1
        prediction.save()
        return prediction
