import {League} from "../../interfaces/league";
import { Modal, Button, Form } from "react-bootstrap";
import React, { useState, useEffect } from "react";
import axiosInstance from "../../axios";

export const AddMyLeagueComponent: React.FC = () => {
    const [leagues, setLeagues] = useState<League[]>([]);
    const [selectedLeagues, setSelectedLeagues] = React.useState();
    const [myLeagueName, setMyLeagueName] = useState("");

    function addSelectedLeagues(event:any) {
        const selectedOptions:any = [...event.target.selectedOptions].map(o => o.value);
        setSelectedLeagues(selectedOptions);
    }

    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const getLeagues = async () => {
      axiosInstance
        .get(`/league/`)
        .then((res) => {
          setLeagues(res.data);
        })
        .catch((error) => console.error(error));
  
    };
    
    const addMyLeague = async () => {
        axiosInstance
        .post('myleague/', {name:myLeagueName, "leagueCodes": selectedLeagues})
        .then((res) => {
            console.log(res);
          })
          .catch((error) => console.error(error));
    }

    useEffect(() => {
      getLeagues();
    }, []);

    return (
            <Form>
                <Form.Group controlId="myLeagueForm.name">
                    <Form.Label>MyLeague name</Form.Label>
                    <Form.Control 
                    type="name"
                    onChange={evt => setMyLeagueName(evt.target.value)}
                    placeholder="Enter MyLeague name" />
                </Form.Group>
                <Form.Group controlId="myLeagueForm.leagues">
                    <Form.Label>Select football leagues to play</Form.Label>
                    <Form.Control
                    as="select" 
                    onChange={event => addSelectedLeagues(event)}
                    multiple
                    >
                    {leagues.map((v, i) => {
                        let league = v as League;
                            return <option value={v.leagueCode}>{v.name}</option>
                    })}
                    </Form.Control>
                    <br/>
                    <Button onClick={addMyLeague}> Create MyLeague </Button>
                </Form.Group>
            </Form>
    );
};
