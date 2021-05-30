"""Stores models"""

from django.db import models
from django.contrib.auth.models import User


class League(models.Model):
    LEAGUES = [
        ("PL", "Premier League"),
        ("PD", "La Liga"),
        ("SA", "Serie A"),
        ("BL1", "Bundesliga"),
        ("FL1", "Ligue 1"),
    ]
    leagueCode = models.CharField(
        max_length=8,
        choices=LEAGUES,
        unique=True,
        verbose_name="league code",
        primary_key=True,
    )
    name = models.CharField(max_length=56)
    logo = models.URLField(null=True)

    def __str__(self):
        return f"{self.name}"


class Team(models.Model):
    teamId = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=56)
    league = models.ForeignKey(
        League, on_delete=models.CASCADE, related_name="teams", null=True
    )
    logo = models.URLField()
    form = models.CharField(max_length=12)
    position = models.IntegerField()
    playedGames = models.IntegerField()
    won = models.IntegerField()
    lost = models.IntegerField()
    draw = models.IntegerField()
    points = models.IntegerField()
    goalsScored = models.IntegerField()
    goalsAgainst = models.IntegerField()
    goalDifference = models.IntegerField()

    def __str__(self):
        return f"{self.name}"


class Matchday(models.Model):
    leagueCode = models.ForeignKey(
        League, on_delete=models.DO_NOTHING, verbose_name="league"
    )
    number = models.IntegerField()

    class Meta:
        unique_together = ("leagueCode", "number")

    def __str__(self):
        return f"{self.leagueCode} {self.number}"


class Match(models.Model):
    matchId = models.CharField(max_length=32, unique=True)
    homeTeam = models.ForeignKey(
        Team,
        on_delete=models.DO_NOTHING,
        related_name="homeTeam",
        verbose_name="home team",
    )
    awayTeam = models.ForeignKey(
        Team,
        on_delete=models.DO_NOTHING,
        related_name="awayTeam",
        verbose_name="away team",
    )
    league = models.ForeignKey(
        League, on_delete=models.DO_NOTHING, verbose_name="league"
    )
    matchday = models.ForeignKey(
        Matchday, on_delete=models.CASCADE, related_name="matches"
    )
    homeTeamScore = models.IntegerField(null=True)
    awayTeamScore = models.IntegerField(null=True)
    date = models.DateField()
    time = models.TimeField()
    result = models.CharField(max_length=56, null=True)
    status = models.CharField(max_length=12)

    def __str__(self):
        return f"{self.homeTeam} - {self.awayTeam} result = {self.result}"


class MyLeague(models.Model):
    name = models.CharField(max_length=56, unique=True)
    myLeagueId = models.CharField(max_length=8, unique=True)
    leagues = models.ManyToManyField(League, verbose_name="league")
    players = models.ManyToManyField(User, verbose_name="players")

    def __str__(self):
        return f"{self.name}"

    def get_league_codes(self):
        leagues = self.leagues.all()
        leagueCodes = []
        for league in leagues:
            leagueCodes.append(league.leagueCode)
        return leagueCodes


class Prediction(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    myLeague = models.ForeignKey(
        MyLeague, on_delete=models.CASCADE, null=True
    )  # do zmiany!
    prediction = models.CharField(max_length=56)
    points = models.IntegerField(default=0)
