// PageVueGlobale.js
import React, { useState, useContext } from 'react';
import WeatherApp from '../weatherapp';
import { SiteContext } from '../ContexteSelectionSite';


function PageVueGlobale() {
    const { selectedSite, setSelectedSite, selectedWorkshop, setSelectedWorkshop } = useContext(SiteContext);

    const handleSiteChange = (newSite) => {
        selectSite(newSite);
    };

    const [isActive, setIsActive] = React.useState(false);

    React.useEffect(() => {
        setIsActive(true);
    }, []);

    return (
        <>
            <div className={`header-vue-globale ${isActive ? 'active' : ''}`}>
            </div>
        <WeatherApp/>
        </>

    );
}

export default PageVueGlobale;
