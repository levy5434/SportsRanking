import { MyLeague }  from "../../interfaces/myLeague";
import { Nav, Card, Modal, Button, Form, Container, Row } from "react-bootstrap";
import React, { useState, useEffect } from "react";
import axiosInstance from "../../axios";
import { LeagueComponent } from "../LeagueComponent/LeagueComponent";
import { AddMyLeagueComponent } from "./AddMyLeagueComponent";

export const MyLeagueComponent: React.FC = () => {
  const [myLeagues, setMyLeagues] = useState<MyLeague[]>([]);
  const [show, setShow] = useState(false);
  const [showJoin, setShowJoin] = useState(false);
  const [myLeagueId, setMyLeagueId] = useState("");
  const [leagueCodes, setLeagueCodes] = useState<string[]>()
  //Join MyLeague Modal
  const handleShowJoin = () => setShowJoin(true);
  const handleCloseJoin = () => setShowJoin(false);
  
  //Create MyLeague
  const handleShow = () => setShow(true);
  const handleClose = () => setShow(false);

  //Join MyLeague
  const addPlayer = async () => {
    let url:string = 'addplayer/'+myLeagueId;
    axiosInstance
    .post(url)
    .then((res) => {
        console.log(res.status);
      })
      .catch((error) => console.error(error));
    }
  
  //Get MyLeagues
  const getMyLeagues = async () => {
    axiosInstance
      .get(`/myleague/`)
      .then((res) => {
        setMyLeagues(res.data);
      })
      .catch((error) => console.error(error));

  };

  useEffect(() => {
    getMyLeagues();
  }, []);

  return (
    <div className="container">
    <Card border="dark" style={{ width: '100%' }}>
        <Card.Header>MyLeagues</Card.Header>
        <Card.Body>
            <Card.Title>Choose your MyLeague</Card.Title>
            <Card.Text>
                <Nav fill variant="tabs" defaultActiveKey="/">
                    {myLeagues.map((v, i) => {
                        let myLeague = v as MyLeague;
                            return (
                            <Nav.Item>
                                <Button variant="light" onClick={() => setLeagueCodes(myLeague.leagueCodes)}>
                                    {myLeague.name} : {myLeague.myLeagueId}
                                </Button>
                            </Nav.Item>
                        )})}
                    <Nav.Item>
                        <Button variant="light" onClick={handleShow}>
                            Create MyLeague
                        </Button>
                    </Nav.Item>
                    <Nav.Item>
                        <Button variant="light" onClick={handleShowJoin}>
                            Join MyLeague
                        </Button>
                    </Nav.Item>
                </Nav>
            </Card.Text>
        </Card.Body>
    </Card>
  <br />
    <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
            <Modal.Title>Create MyLeague</Modal.Title>
        </Modal.Header>
        <Modal.Body>
            <AddMyLeagueComponent />
        </Modal.Body>
        <Modal.Footer>
            <Button variant="secondary" onClick={handleClose}>Close</Button>
            <Button variant="primary">Save changes</Button>
        </Modal.Footer>
    </Modal>
    <Modal show={showJoin} onHide={handleCloseJoin}>
        <Modal.Header closeButton>
            <Modal.Title>Join MyLeague</Modal.Title>
        </Modal.Header>
        <Modal.Body>
            <Form>
                <Form.Group controlId="myLeagueForm.Id">
                    <Form.Label>MyLeague ID</Form.Label>
                    <Form.Control type="name" 
                    onChange={evt => setMyLeagueId(evt.target.value)}
                    placeholder="Enter MyLeague ID" />
                </Form.Group>
            </Form>
        </Modal.Body>
        <Modal.Footer>
            <Button variant="secondary" onClick={handleCloseJoin}>Close</Button>
            <Button
            className="btnFormSend"
            variant="primary"
            onClick={addPlayer}
            >
            Join MyLeague</Button>
        </Modal.Footer>
    </Modal>
    <Container>
        <Row>
        {leagueCodes ? leagueCodes.map((v, i) =>{
                let leagueCode = v as string;
                    return (<LeagueComponent leagueCode={leagueCode} />)
                })
                :null}
        </Row>
    </Container>
    </div>
  );
};
