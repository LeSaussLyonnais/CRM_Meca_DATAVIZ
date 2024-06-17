import React, { useContext, useEffect, useState } from 'react';
import sedeconnecter from '../Assets/sedeconnecter.png';
import accueil from '../Assets/accueil.png'; // Importer l'image accueil
import { SiteContext } from './ContexteSelectionSite';
import '../Styles/sidebar.css';

function Sidebar({ isOpen, toggleSidebar }) {
    const [SitesDisponibles, setSitesDisponibles] = useState([]);
    const [AllAteliers, setAllAteliers] = useState({});
    const { selectedSite, setSelectedSite, selectedWorkshop, setSelectedWorkshop } = useContext(SiteContext);

    useEffect(() => {
        fetchSite();
    }, []);

    useEffect(() => {
        if (SitesDisponibles && SitesDisponibles.Sites) {
            SitesDisponibles.Sites.forEach((site) => {
                if (site.COSECT) {
                    fetchAtelier(site);
                }
            });
        }
    }, [SitesDisponibles]);

    const fetchSite = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/BlogApp/getSite', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            const data = await response.json();
            console.log(data);
            setSitesDisponibles(data);
        } catch (error) {
            console.error('Error fetching sites:', error);
        }
    };

    const fetchAtelier = async (site) => {
        try {
            const response = await fetch('http://127.0.0.1:8000/BlogApp/getAtelier', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    site: site.COSECT,
                }),
            });
            const data = await response.json();
            console.log(data);
            setAllAteliers((prevAteliers) => ({
                ...prevAteliers,
                [site.Libelle_Site]: data.Ateliers.map((atelier) => atelier.Libelle_Atelier),
            }));
        } catch (error) {
            console.error('Error fetching ateliers:', error);
        }
    };

    const handleWorkshopClick = (workshop, site) => {
        setSelectedSite(SitesDisponibles.Sites.find(item =>item.Libelle_Site === site))
        setSelectedWorkshop({"Libelle_Atelier":workshop});
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
                    {Object.keys(AllAteliers).map((site, index) => (
                        <React.Fragment key={index}>
                            <li className="site" onClick={() => setSelectedSite(SitesDisponibles.Sites.find(item =>item.Libelle_Site === site))}>{site}</li>
                            {AllAteliers[site].map((atelier, idx) => (
                                <li key={idx} className="atelier" onClick={() => handleWorkshopClick(atelier, site)}>
                                    {atelier}
                                </li>
                            ))}
                        </React.Fragment>
                    ))}
                </ul>
            </div>
        </div>
    );
}

export default Sidebar;
