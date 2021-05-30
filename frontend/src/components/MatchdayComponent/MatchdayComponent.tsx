import { Match } from "../../interfaces/match";
import { Table } from "react-bootstrap";
import React, { useState, useEffect } from "react";
import { MatchComponent } from "../MatchComponent/MatchComponent";
import axiosInstance from "../../axios";

export const MatchdayComponent: React.FC<{ number: string }> = () => {
  const [matches, setMatches] = useState<Match[]>([]);

  const getMatchday = async () => {
    axiosInstance
      .get(`/matchday/1`)
      .then((res) => {
        setMatches(res.data.matches);
      })
      .catch((error) => console.error(error));

  };

  useEffect(() => {
    getMatchday();
  }, []);

  return (
    <div className="container">
      <h1>Matches</h1>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>Date</th>
            <th>Home Team</th>
            <th>Away Team</th>
            <th>Result</th>
          </tr>
        </thead>
        <tbody>
          {matches.map((v, i) => {
            let match = v as Match;
            return <MatchComponent match={match} key={match.matchId} />;
          })}
        </tbody>
      </Table>
    </div>
  );
};
