import React, { useContext, useEffect, useState } from 'react';
import { SiteContext } from '../ContexteSelectionSite';
import '../../Styles/StylePageSelection.css';
import BasPageImage from '../../Assets/BasPage.png';

function PageSelection() {
  const { selectedSite, setSelectedSite, selectedWorkshop, setSelectedWorkshop } = useContext(SiteContext);
  const [ateliers, setAteliers] = useState([]);
  const ateliersDisponibles = ['Usinage', 'Mécano soudure', 'Peinture', 'Retouches', 'Assemblage', 'Contrôle'];
  const sitesDisponibles = ['Blaye-Les-Mines', 'Site 2', 'Site 3'];

  useEffect(() => {
    if (selectedSite) {
      const ateliersAleatoires = [];
      const nombreAteliers = Math.floor(Math.random() * (4 - 1 + 1)) + 1; // Entre 1 et 4 ateliers

      for (let i = 0; i < nombreAteliers; i++) {
        const randomIndex = Math.floor(Math.random() * ateliersDisponibles.length);
        ateliersAleatoires.push(ateliersDisponibles[randomIndex]);
        ateliersDisponibles.splice(randomIndex, 1); // Retirer l'atelier sélectionné de la liste des ateliers disponibles
      }

      setAteliers(ateliersAleatoires);
    } else {
      setSelectedWorkshop(null);
    }
  }, [selectedSite]);

  const handleSiteClick = (site) => {
    setSelectedSite(site);
    setSelectedWorkshop(null);
  };

  const handleWorkshopClick = (workshop) => {
    setSelectedWorkshop(workshop);
  };

  return (
    <div className="page-selection-container">
      <h1 className="title">Bonjour !</h1>
      <p className="description">
        Bienvenue dans le Dashboard de suivi de production, veuillez choisir un atelier à parcourir :
      </p>
      <hr className="divider" />

      <div className="container-rectanglechoix">
        <div className="rectanglechoix show">
          <div className='col-12 d-flex flex-column justify-content-center align-items-start gap-4 mt-2'>
            <h2>Choix du site</h2>
            <div className='trait-site'></div>
          </div>
          <div>
            <div className="liste-sites">
              <ul>
                {sitesDisponibles.map((site, index) => (
                  <li key={index} className={selectedSite === site ? 'active' : ''} onClick={() => handleSiteClick(site)} style={{marginBottom:(6/sitesDisponibles.length)+'rem'}}>{site}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
        {selectedSite && (
          <div className={`rectanglechoix ${selectedSite ? 'show' : 'hide'}`}>
            <div className='col-12 d-flex flex-column justify-content-center align-items-start gap-4 mt-2'>
              <h2>Choix de l'atelier</h2>
              <div className='trait-site'></div>
            </div>
            <div>
              <div className="liste-ateliers">
                <ul className='d-flex flex-column justify-content-start align-items-start'>
                  {ateliers.map((atelier, index) => (
                    <li key={index} className={selectedWorkshop === atelier ? 'active' : ''} onClick={() => handleWorkshopClick(atelier)} style={{marginBottom:(6/ateliers.length)+'rem'}}>{atelier}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
      <img src={BasPageImage} alt="Bas de page" className="bas-page" />
    </div>
  );
}

export default PageSelection;
