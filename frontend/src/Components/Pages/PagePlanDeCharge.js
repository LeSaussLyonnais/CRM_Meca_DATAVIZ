// PageOrdonnancement.js
import React, { useState } from 'react';
import FullWidthTabs from '../BarreSites';
import { useSiteSelection } from '../SiteSelectionContext';

function PagePlanDeCharge() {
    const [ selectedSite, selectSite ] = useState(useSiteSelection());

    const handleSiteChange = (newSite) => {
        selectSite(newSite);
    };

    const [isActive, setIsActive] = React.useState(false);

    React.useEffect(() => {
        setIsActive(true);
    }, []);

    return (
        <div className={`header-plandecharge ${isActive ? 'active' : ''}`}>
            <FullWidthTabs selectedSite={selectedSite} onSiteChange={handleSiteChange} />
        </div>
    );
}

export default PagePlanDeCharge;
