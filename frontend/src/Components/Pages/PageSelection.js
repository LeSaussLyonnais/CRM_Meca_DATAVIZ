import React, { useContext, useEffect, useState } from 'react';
import { SiteContext } from '../ContexteSelectionSite';
import '../../Styles/selectionatelier.css';
import BasPageImage from '../../Assets/BasPage.png';
import ColorModifiedImage from '../ColorPngChange';
import { CiCirclePlus } from "react-icons/ci";
import ModalAjout from '../Selection/ModalAjout';

function PageSelection() {
  const { selectedSite, setSelectedSite, selectedWorkshop, setSelectedWorkshop } = useContext(SiteContext);
  const [ateliers, setAteliers] = useState([]);
  const [PosteDisponibles, setPosteDisponibles] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [SitesDisponibles, setSitesDisponibles] = useState(['Blaye-Les-Mines', 'Site 2', 'Site 3']);
  const [AteliersDisponibles, setAteliersDisponibles] = useState(['Usinage', 'Mécano soudure', 'Peinture', 'Retouches', 'Assemblage', 'Contrôle']);

  useEffect(() => {
    if (selectedSite) {
      const ateliersAleatoires = [];
      const nombreAteliers = Math.floor(Math.random() * (4 - 1 + 1)) + 1;

      for (let i = 0; i < nombreAteliers; i++) {
        const randomIndex = Math.floor(Math.random() * AteliersDisponibles.length);
        ateliersAleatoires.push(AteliersDisponibles[randomIndex]);
        AteliersDisponibles.splice(randomIndex, 1);
      }

      setAteliersDisponibles(ateliersAleatoires);
    } else {
      setAteliersDisponibles([...AteliersDisponibles]);
      setSelectedWorkshop(null);
    }
  }, [selectedSite]);

  useEffect(() => {
    fetchSite();
    fetchAtelier();
  }, []);

  const handleSiteClick = (site) => {
    setSelectedSite(site);
    setSelectedWorkshop(null);
  };

  const handleWorkshopClick = (workshop) => {
    setSelectedWorkshop(workshop);
  };

  const handleClick = () => {
    setShowModal(true);
    fetchPostes();
  }

  const fetchPostes = async () => {
    try {
      const response = await fetch('http://localhost:8000/BlogApp/PopupAjoutAtelier/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          site: selectedSite,
        }),
      });
      const data = await response.json();
      setPosteDisponibles(data);
    }
    catch (error) {
      console.error('Error fetching postes:', error);
    }
  }

  const fetchSite = async () => {
    try {
      const response = await fetch('http://localhost:8000/BlogApp/getSite/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      const data = await response.json();
      const tempSiteList = [...SitesDisponibles, ...data];
      setSitesDisponibles(tempSiteList);
    }
    catch (error) {
      console.error('Error fetching postes:', error);
    }
  }
  const fetchAtelier = async () => {
    try {
      const response = await fetch('http://localhost:8000/BlogApp/getAtelier/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          site: selectedSite,
        })
      });
      const data = await response.json();
      const tempAtelierList = [...AteliersDisponibles, ...data];
      setAteliersDisponibles(tempAtelierList);
    }
    catch (error) {
      console.error('Error fetching postes:', error);
    }
  }

  return (
    <div className="page-selection-container">
      <h1 className="title">Bonjour !</h1>
      <p className="description">
        Bienvenue dans le Dashboard de suivi de production, veuillez choisir un atelier à parcourir :
      </p>
      <hr className="divider" />

      <div className="container-rectanglechoix">
        <div className="rectanglechoix">
          <div className='col-12 d-flex flex-column justify-content-center align-items-start gap-4 mt-2'>
            <h2>Choix du site</h2>
            <div className='trait-site'></div>
          </div>
          <div>
            <div className="liste-sites">
              <ul>
                {SitesDisponibles.map((site, index) => (
                  <li key={index} className={selectedSite === site ? 'active' : ''} onClick={() => handleSiteClick(site)} style={{ marginBottom: (6 / SitesDisponibles.length) + 'rem' }}>{site}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
        <div className={`rectanglechoix choix-atelier ${selectedSite ? 'show' : ''}`}>
          <div className='col-12 d-flex flex-column justify-content-center align-items-start gap-4 mt-2'>
            <div className='col-12 d-flex flex-row justify-content-between align-items-center px-4'>
              <h2 className='p-0 m-0'>Choix de l'atelier</h2>
              <CiCirclePlus className="btn-perso-add" onClick={() => handleClick()} />
            </div>
            <div className='trait-site'></div>
          </div>
          <div>
            <div className="liste-ateliers">
              <ul className='d-flex flex-column justify-content-start align-items-start'>
                {AteliersDisponibles.map((atelier, index) => (
                  <li key={index} className={selectedWorkshop === atelier ? 'active' : ''} onClick={() => handleWorkshopClick(atelier)} style={{ marginBottom: (6 / AteliersDisponibles.length) + 'rem' }}>{atelier}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
      <img src={BasPageImage} alt="Bas de page" className="bas-page" />
      <ModalAjout show={showModal} setshow={setShowModal} site={selectedSite} AllDispoPoste={PosteDisponibles} />
    </div>
  );
}

export default PageSelection;
