import {React, useState} from 'react';
import { Link } from 'react-router-dom';


import WelcomePage from './pages/welcomePage';
import LogInPage from './pages/LogInPage';
import JoinPage from './pages/JoinPage';
import './App.css';

import { BrowserRouter, Route, Switch } from 'react-router-dom';
import styled from 'styled-components';

function App() {


  return (
    <BrowserRouter>
    <div className="App">
      <div className="full">
        <Switch>
          <Route exact path ="/" component={WelcomePage}/>
          <Route exact path="/login" component={LogInPage} />
          <Route exact path="/join" component={JoinPage} />
        </Switch>
      </div>
    </div>
    </BrowserRouter>
    
  );
}

export default App;
