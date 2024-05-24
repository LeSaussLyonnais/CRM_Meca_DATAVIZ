import React, { useContext, useEffect, useState } from 'react';
import { SiteContext } from '../ContexteSelectionSite';
import '../../Styles/selectionatelier.css';
import BasPageImage from '../../Assets/BasPage.png';
import ColorModifiedImage from '../ColorPngChange';
import { CiCirclePlus } from "react-icons/ci";
import ModalAjout from '../Selection/ModalAjout';

function PageSelection() {
  const { selectedSite, setSelectedSite, selectedWorkshop, setSelectedWorkshop } = useContext(SiteContext);
  const [new_ateliers, setNewAteliers] = useState(false);
  const [PosteDisponibles, setPosteDisponibles] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [SitesDisponibles, setSitesDisponibles] = useState([]);
  const [AteliersDisponibles, setAteliersDisponibles] = useState(['Usinage', 'Mécano soudure', 'Peinture', 'Retouches', 'Assemblage', 'Contrôle']);

  useEffect(() => {
    if (selectedSite) {
      fetchAtelier();
      setNewAteliers(false);
    } else {
      setAteliersDisponibles([]);
      setSelectedWorkshop(null);
      setNewAteliers(false);
    }
  }, [selectedSite, new_ateliers]);

  useEffect(() => {
    fetchSite();
  }, []);

  const handleSiteClick = (site) => {
    setSelectedSite(site);
    setSelectedWorkshop(null);
  };

  const handleWorkshopClick = (workshop) => {
    setSelectedWorkshop(workshop);
  };

  const handleClick = () => {
    fetchPostes();
    setShowModal(true);
  }

  const fetchPostes = async () => {
    try {
      const response = await fetch('http://localhost:8000/BlogApp/PopupAjoutAtelier', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          site: selectedSite.COSECT,
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
      const response = await fetch('http://localhost:8000/BlogApp/getSite', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      const data = await response.json();
      console.log(data);
      // const tempSiteList = [...SitesDisponibles, ...data];
      setSitesDisponibles(data);
    }
    catch (error) {
      console.error('Error fetching sites:', error);
    }
  }
  const fetchAtelier = async () => {
    try {
      const response = await fetch('http://localhost:8000/BlogApp/getAtelier', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          site: selectedSite.COSECT,
        })
      });
      const data = await response.json();
      setAteliersDisponibles(data);
    }
    catch (error) {
      console.error('Error fetching ateliers:', error);
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
                {SitesDisponibles && SitesDisponibles.Sites && SitesDisponibles.Sites.map((site, index) => (
                  <li key={index} className={(selectedSite && selectedSite.COSECT === site.COSECT ) ? 'active' : ''} onClick={() => handleSiteClick(site)} style={{ marginBottom: (6 / SitesDisponibles.Sites.length) + 'rem' }}>{site.Libelle_Site}</li>
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
                {AteliersDisponibles && AteliersDisponibles.Ateliers && AteliersDisponibles.Ateliers.map((atelier, index) => (
                  <li key={index} className={selectedWorkshop && selectedWorkshop.Libelle_Atelier === atelier.Libelle_Atelier ? 'active' : ''} onClick={() => handleWorkshopClick(atelier)} style={{ marginBottom: (6 / AteliersDisponibles.Ateliers.length) + 'rem' }}>{atelier.Libelle_Atelier}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
      <img src={BasPageImage} alt="Bas de page" className="bas-page" />
      <ModalAjout show={showModal} setshow={setShowModal} site={selectedSite} AllDispoPoste={PosteDisponibles} setNewAteliers={setNewAteliers}/>
    </div>
  );
}

export default PageSelection;
