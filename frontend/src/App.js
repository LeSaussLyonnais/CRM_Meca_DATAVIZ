import React, { useContext } from 'react';
import logo from "./Assets/logo_acti.png";
import Navbar from "./Components/Navbar";
import PageSelection from "./Components/Pages/PageSelection";
import PageVueGlobale from "./Components/Pages/PageVueGlobale";
import PageVueMachine from './Components/Pages/PageVueMachine';
import PagePlanDeCharge from './Components/Pages/PagePlanDeCharge';
import PageCommunication from './Components/Pages/PageCommunication';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import "bootstrap/dist/css/bootstrap.min.css";
import { SiteContext } from './Components/ContexteSelectionSite';


function App() {
  const { selectedSite, setSelectedSite, selectedWorkshop, setSelectedWorkshop } = useContext(SiteContext);

  return (
    <Router>
      <div className="app-container">
        <header>
          <img src={logo} alt="logo_acti.png" className="logo" />
          <Navbar />
        </header>
        <div className="main">
          <Routes>
            <Route path="/" element={<PageSelection />} />
            {
              selectedSite && selectedWorkshop && <>
                <Route path='/VueGlobale' element={<PageVueGlobale />} />
                <Route path='/VueMachine' element={<PageVueMachine />} />
                <Route path='/Communication' element={<PageCommunication />} />
                <Route path='/PlanDeCharge' element={<PagePlanDeCharge />} />
              </>
            }
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
