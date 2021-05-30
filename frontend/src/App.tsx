import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Route } from "react-router-dom";
import Header from "./components/Header";
import Login from "./components/Login";
import Logout from "./components/Logout";
import { MatchComponent } from "./components/MatchComponent/MatchComponent";
import { MatchdayComponent } from "./components/MatchdayComponent/MatchdayComponent";
import { AddMyLeagueComponent } from "./components/MyLeagueComponent/AddMyLeagueComponent";
import { MyLeagueComponent } from "./components/MyLeagueComponent/MyLeagueComponent";
import Register from "./components/Register";
import jwt_decode from 'jwt-decode';

function App() {

  
  return (
    <Router>
      <div className="App">
        <Header/>
        <div className="container mx-auto">
          <Route path="/register" exact component={Register} />
          <Route path="/login" exact component={Login} />
          <Route path="/logout" exact component={Logout} />
          <Route path="/myleagues" exact component={MyLeagueComponent} />
          <Route path="/myleagues/create" exact component={AddMyLeagueComponent} />
        </div>
      </div>
    </Router>
  );
}

export default App;
