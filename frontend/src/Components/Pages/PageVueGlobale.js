// PageVueGlobale.js
import React, { useState } from 'react';
import FullWidthTabs from '../BarreSites';
import { useSiteSelection } from '../SiteSelectionContext';
import WeatherApp from '../weatherapp';

function PageVueGlobale() {
    const [selectedSite, selectSite] = useState(useSiteSelection());

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
                <FullWidthTabs selectedSite={selectedSite} onSiteChange={handleSiteChange} />
            </div>
        <WeatherApp/>
        </>

    );
}

export default PageVueGlobale;
