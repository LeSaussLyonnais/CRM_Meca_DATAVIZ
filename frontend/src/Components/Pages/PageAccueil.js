// PageAccueil.js
import React from 'react';
import MenuAccueil from '../MenuAccueil';
import Bienvenue from '../Bienvenue'; // Importez le composant Bienvenue ici
import { useSiteSelection } from '../SiteSelectionContext';

function PageAccueil() {
  const { selectSite } = useSiteSelection();

  const handleSiteClick = (site) => {
    selectSite(site);
  };

  return (
    <div>
      <Bienvenue /> {/* Inclure le composant Bienvenue ici */}
      <MenuAccueil onSiteClick={handleSiteClick} />
    </div>
  );
}

export default PageAccueil;
