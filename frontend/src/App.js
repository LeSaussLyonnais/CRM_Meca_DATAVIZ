import React from 'react';
import logo from "./Assets/logo_acti.png";
import Navbar from "./Components/Navbar";
import PageSelection from "./Components/Pages/PageSelection";
import PageVueGlobale from "./Components/Pages/PageVueGlobale";
import PageVuePoste from './Components/Pages/PageVuePoste';
import PagePlanDeCharge from './Components/Pages/PagePlanDeCharge';
import './Styles/vueposte.css'
import './Styles/vueglobale.css'
import './Styles/plandecharge.css'
// import PageCommunication from './Components/Pages/PageCommunication';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import "bootstrap/dist/css/bootstrap.min.css";
import { SiteProvider } from './Components/ContexteSelectionSite';
import PageCommunication from './Components/Pages/PageCommunication';

function App() {
  return (
    <Router>
      <SiteProvider>
        <div className="app-container">
          <header>
            <img src={logo} alt="logo_acti.png" className="logo" />
            <Navbar />
          </header>
          <div className="main">
            <Routes>
              <Route path="/" element={<PageSelection />} />
              <Route path='/VueGlobale' element={<PageVueGlobale/>} />
              <Route path='/VuePoste' element={<PageVuePoste/>} />
              <Route path='/PlanDeCharge' element={<PagePlanDeCharge/>} />
              <Route path='/Communication' element={<PageCommunication/>} />
            </Routes>
          </div>
        </div>
      </SiteProvider>
    </Router>
  );
}

export default App;
