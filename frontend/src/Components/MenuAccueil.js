import React from 'react';
import BlayeLesMinesImage from '../Assets/BlayeLesMines.png';
import Site2Image from '../Assets/Site2.png';
import Site3Image from '../Assets/Site3.png';
import BasPageImage from '../Assets/BasPage.png';
import { useSiteSelection } from './SiteSelectionContext';

function MenuAccueil() {
    const { selectedSite, selectSite } = useSiteSelection(); // Utilisez useContext pour récupérer les valeurs du contexte

    const handleImageClick = (site) => {
        selectSite(site); // Mettez à jour la sélection du site en utilisant la fonction fournie par le contexte
    };

    return (
        <div className="menu-accueil-container">
            <div className={`container-link ${selectedSite === 'Blaye-Les-Mines' ? 'agrandi' : ''}`} onClick={() => handleImageClick('Blaye-Les-Mines')}>
                <img src={BlayeLesMinesImage} alt="BlayeLesMines" className="BlayeLesMines" />
                <div className="text-overlay-site1">Site de <br /> Blaye-les-mines</div>
            </div>
            
            <div className={`container-link ${selectedSite === 'Site 2' ? 'agrandi' : ''}`} onClick={() => handleImageClick('Site 2')}>
                <img src={Site2Image} alt="Site 2" className="site2" />
                <div className="text-overlay-site2">Site 2</div>
            </div>

            <div className={`container-link ${selectedSite === 'Site 3' ? 'agrandi' : ''}`} onClick={() => handleImageClick('Site 3')}>
                <img src={Site3Image} alt="Site 3" className="site3" />
                <div className="text-overlay-site3">Site 3</div>
            </div>
            
            <img src={BasPageImage} alt="Bas de page" className="bas-page" />
        </div>
    );
}

export default MenuAccueil;
