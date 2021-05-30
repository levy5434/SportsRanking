import json
import http.client
import os


class LeagueApi:
    def __init__(self, leagueCode: str) -> None:
        self.leagueCode = leagueCode
        self.leagueName = None

    def get_teams(self, response):
        standings = self.make_request()
        return [
            {
                "position": team["position"],
                "teamId": team["team"]["id"],
                "name": team["team"]["name"],
                "logo": team["team"]["crestUrl"],
                "form": team["form"],
                "playedGames": team["playedGames"],
                "won": team["won"],
                "draw": team["draw"],
                "lost": team["won"],
                "points": team["won"],
                "goalsScored": team["goalsFor"],
                "goalsAgainst": team["goalsAgainst"],
                "goalDifference": team["goalDifference"],
            }
            for team in standings
        ]

    def make_request(self):
        connection = http.client.HTTPConnection("api.football-data.org")
        headers = {"X-Auth-Token": os.getenv("FOOTBALL_DATA_API_KEY")}
        connection.request(
            "GET",
            f"/v2/competitions/{self.leagueCode}/standings",
            None,
            headers,
        )
        response = json.loads(connection.getresponse().read().decode())
        self.leagueName = response["competition"]["name"]
        return response["standings"][0]["table"]


class MatchdayApi:
    def __init__(self, leagueCode: str, number: int) -> None:
        self.leagueCode = leagueCode
        self.number = number

    def get_matches(self, response):
        matches = self.make_request()
        return [
            {
                "matchId": match["id"],
                "homeTeam": match["homeTeam"]["id"],
                "awayTeam": match["awayTeam"]["id"],
                "date": match["utcDate"][:10],
                "time": match["utcDate"][11:19],
                "winner": match["score"]["winner"],
                "status": match["status"],
                "homeTeamScore": match["score"]["fullTime"]["homeTeam"],
                "awayTeamScore": match["score"]["fullTime"]["awayTeam"],
            }
            for match in matches
        ]

    def make_request(self):
        connection = http.client.HTTPConnection("api.football-data.org")
        headers = {"X-Auth-Token": os.getenv("FOOTBALL_DATA_API_KEY")}
        connection.request(
            "GET",
            f"/v2/competitions/{self.leagueCode}/matches/?matchday={self.number}",  # noqa
            None,
            headers,
        )
        response = json.loads(connection.getresponse().read().decode())
        return response["matches"]
