import React, { createContext, useContext, useState } from 'react';

const SiteSelectionContext = createContext();

export const SiteSelectionProvider = ({ children }) => {
  const [selectedSite, setSelectedSite] = useState(null);

  const selectSite = (site) => {
    setSelectedSite(site);
  };

  return (
    <SiteSelectionContext.Provider value={{ selectedSite, selectSite }}>
      {children}
    </SiteSelectionContext.Provider>
  );
};

export const useSiteSelection = () => {
  const context = useContext(SiteSelectionContext);
  if (!context) {
    throw new Error('useSiteSelection must be used within a SiteSelectionProvider');
  }
  return context;
};
