import React, { useContext } from 'react';
import sedeconnecter from '../Assets/sedeconnecter.png';
import accueil from '../Assets/accueil.png'; // Importer l'image accueil
import { SiteContext } from './ContexteSelectionSite';
import '../Styles/sidebar.css';

function Sidebar({ isOpen, toggleSidebar }) {
    const { selectedSite, setSelectedWorkshop } = useContext(SiteContext);

    const sitesAteliers = {
        'Blaye-Les-Mines': ['Usinage', 'Mécano soudure', 'Peinture'],
        'Site 2': ['Mécano soudure', 'Peinture'],
        'Site 3': ['Usinage', 'Mécano soudure']
    };

    const handleWorkshopClick = (workshop) => {
        setSelectedWorkshop(workshop);
    };

    const handleAccueilClick = () => {
        window.location.href = '/'; // Rediriger vers la page d'accueil
    };

    return (
        <div className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
            <button className="close-btn" onClick={toggleSidebar}>X</button>
            <div className="sidebar-content">
                <button className="home-btn" onClick={handleAccueilClick}>
                    <img src={accueil} alt="Accueil" className="home-icon" />
                    Accueil
                </button>
                <button className="logout-btn">
                    <img src={sedeconnecter} alt="Déconnexion" className="logout-icon" />
                    Se déconnecter
                </button>
                <hr />
                <ul>
                    {Object.keys(sitesAteliers).map((site, index) => (
                        <React.Fragment key={index}>
                            <li className="site">{site}</li>
                            {sitesAteliers[site].map((atelier, idx) => (
                                <li key={idx} className="atelier" onClick={() => handleWorkshopClick(atelier)}>{atelier}</li>
                            ))}
                        </React.Fragment>
                    ))}
                </ul>
            </div>
        </div>
    );
}

export default Sidebar;
