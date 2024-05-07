import React, { useState } from 'react';
import { useSiteSelection } from './SiteSelectionContext';

export default function BarreSites() {
  const { selectedSite, selectSite } = useSiteSelection(); // Utilisez le hook useSiteSelection pour obtenir le contexte

  const [hoveredTab, setHoveredTab] = useState(null);

  const handleTabClick = (site) => { // Modifier pour recevoir le site sélectionné
    selectSite(site); // Mettre à jour le site sélectionné
  };

  const handleTabHover = (tabIndex) => {
    setHoveredTab(tabIndex);
  };

  const handleTabLeave = () => {
    setHoveredTab(null);
  };

  return (
    <div style={{ backgroundColor: '#f0f0f0', padding: '5px', border: '2px solid #B8DDFF', borderBottom: 'none', borderTopLeftRadius: '12px', borderTopRightRadius: '12px', boxShadow: '#B8DDFF 0.3125rem 0.3125rem 0.3125rem 0.125rem', width: '68rem', fontFamily: 'Poppins, sans-serif' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
      
        <div onClick={() => handleTabClick('Blaye-Les-Mines')} onMouseEnter={() => handleTabHover(0)} onMouseLeave={handleTabLeave} 
        style={{ cursor: 'pointer', textAlign: 'center', width: 'calc(100% / 3)', borderRight: '2px solid #B8DDFF', fontWeight: 600, padding: '10px', borderRadius: '8px', backgroundColor: (selectedSite === 'Blaye-Les-Mines' || hoveredTab === 0) ? '#DBE8F4' : 'transparent', transition: 'background-color 0.3s' }}>Site de Blaye-Les-Mines</div>
       
        <div onClick={() => handleTabClick('Site 2')} onMouseEnter={() => handleTabHover(1)} onMouseLeave={handleTabLeave} 
        style={{ cursor: 'pointer', textAlign: 'center', width: 'calc(100% / 3)', borderRight: '2px solid #B8DDFF', fontWeight: 600, padding: '10px', borderRadius: '8px', backgroundColor: (selectedSite === 'Site 2' || hoveredTab === 1) ? '#DBE8F4' : 'transparent', transition: 'background-color 0.3s' }}>Site 2</div>
        
        <div onClick={() => handleTabClick('Site 3')} onMouseEnter={() => handleTabHover(2)} onMouseLeave={handleTabLeave} 
        style={{ cursor: 'pointer', textAlign: 'center', width: 'calc(100% / 3)', fontWeight: 600, padding: '10px', borderRadius: '8px', backgroundColor: (selectedSite === 'Site 3' || hoveredTab === 2) ? '#DBE8F4' : 'transparent', transition: 'background-color 0.3s' }}>Site 3</div>
      </div>
    </div>
  );
}
