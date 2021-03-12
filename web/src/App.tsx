import React from 'react';
import './App.css';

import Header from './Header';
import Footer from './Footer';
import Home from './Pages/Home/Home';
import Survey from './Pages/Survey/Survey';
import Page404 from './Pages/Page404';

import {
  BrowserRouter as Router,
  Switch,
  Route
} from 'react-router-dom';

export default function App() {
  return (
    <div className="App">
      <Header/>
      <Router>
        <div>
          <Switch>
            <Route path="/surveys/:surveyKey" component={Survey}/>
            <Route exact path="/" component={Home}/>
            <Route path="page404" component={Page404}/>
            <Route component={Page404}/>
          </Switch>
        </div>
      </Router>
      <Footer/>
    </div>
  );
}
