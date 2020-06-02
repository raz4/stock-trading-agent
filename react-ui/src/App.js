import React from 'react';
import './App.css';
import Header from './components/Header';
import Home from './components/Home';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

function About() {
  return <h2>In progress...</h2>;
}

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {currentPage: new Date()};
  }

  render() {
    return (
      <div className="App">
        <Router>
          <Header />

          <Switch>
            <Route exact={true} path="/">
              <Home />
            </Route>
            <Route path="/about">
              <About />
            </Route>
          </Switch>
        </Router>
      </div>
    );
  }
}

export default App;
