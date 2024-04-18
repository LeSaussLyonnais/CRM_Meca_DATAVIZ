// App.js
import React from 'react';
import { SiteSelectionProvider } from './Components/SiteSelectionContext';
import logo from "./Assets/logo_crm.png";
import Navbar from "./Components/Navbar";
import PageAccueil from "./Components/Pages/PageAccueil";
import PageVueGlobale from "./Components/Pages/PageVueGlobale";
import PageOrdonnancement from "./Components/Pages/PageOrdonnancement";
import PagePlanDeCharge from "./Components/Pages/PagePlanDeCharge";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import "bootstrap/dist/css/bootstrap.min.css";
import './Styles/styles.css';
import './Styles/vueglobale.css';
import './Styles/ordonnancement.css';
import './Styles/plandecharge.css';

function App() {
  return (
    <Router>
      <SiteSelectionProvider>
        <div className="app-container">
          <header>
            <img src={logo} alt="logo_crm.png" className="logo" />
            <Navbar />
          </header>
          <div className="main">
            <Routes>
              <Route path="/" element={<PageAccueil />} />
              <Route path="/VueGlobale" element={<PageVueGlobale />} />
              <Route path="/Ordonnancement" element={<PageOrdonnancement />} />
              <Route path="/PlanDeCharge" element={<PagePlanDeCharge />} />
            </Routes>
          </div>
        </div>
      </SiteSelectionProvider>
    </Router>
  );
}

export default App;
