// ContexteSelectionSite.js
import React, { createContext, useState } from 'react';

const SiteContext = createContext();

const SiteProvider = ({ children }) => {
  const [selectedSite, setSelectedSite] = useState(null);
  const [selectedWorkshop, setSelectedWorkshop] = useState(null); // Assurez-vous que selectedWorkshop est défini et initialisé
  // Ajoutez selectedWorkshop dans la valeur du contexte
  return (
    <SiteContext.Provider value={{ selectedSite, setSelectedSite, selectedWorkshop, setSelectedWorkshop }}>
      {children}
    </SiteContext.Provider>
  );
};

export { SiteProvider, SiteContext };
