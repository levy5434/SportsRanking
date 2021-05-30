import React, { useState, useEffect } from "react";
import { Table } from "react-bootstrap";
import { Match } from "../../interfaces/match";

type MatchComponentProps = {
  match: Match;
};
export const MatchComponent: React.FC<MatchComponentProps> = ({match,}: MatchComponentProps) => {
  return (
    <tr>
      <td>
        {match.time} {match.date}
      </td>
      <td>{match.homeTeamName}</td>
      <td>{match.awayTeamName}</td>
      <td>{match.result}</td>
    </tr>
  );
};
