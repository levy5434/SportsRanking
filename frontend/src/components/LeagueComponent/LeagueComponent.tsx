import {League} from "../../interfaces/league";
import React, { useState, useEffect } from "react";
import axiosInstance from "../../axios";
import { Col } from "react-bootstrap";
import Image from 'react-bootstrap/Image'

export const LeagueComponent: React.FC<{leagueCode:string}> = ({leagueCode}) => {
  const [league, setLeague] = useState<League>();

  const getLeagues = async () => {
    axiosInstance
      .get(`/league/`+leagueCode)
      .then((res) => {
        setLeague(res.data);
      })
      .catch((error) => console.error(error));

  };

  useEffect(() => {
    getLeagues();
  }, []);

  return (
    <Col xs lg="2">
      {league ? 
        <Image src={league.logo} 
        fluid/>:null}
    </Col>
  );
};
