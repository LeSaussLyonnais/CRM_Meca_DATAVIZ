// PageVueGlobale.js
import React, { useState, useEffect, useContext } from 'react';
// import WeatherApp from '../weatherapp';
import { SiteContext } from '../ContexteSelectionSite';
import GraphAffaire from '../VueGlobal/GraphAffaire';
import TRS from '../VueGlobal/TRS';
import RendementProd from '../VueGlobal/RendementProd';


function PageVueGlobale() {
    const { selectedSite, setSelectedSite, selectedWorkshop, setSelectedWorkshop } = useContext(SiteContext);
    const [AllAffaireData, setAllAffaireData] = useState([]);
    const [AllRendementData, setAllRendementData] = useState([]);
    const [AllTRSData, setAllTRSData] = useState([]);

    const handleSiteChange = (newSite) => {
        selectSite(newSite);
    };

    const [isActive, setIsActive] = useState(false);

    useEffect(() => {
        setIsActive(true);
    }, []);

    return (
        <div className='container-fluid d-flex justify-content-center align-items-center flex-column mb-5 mt-4 px-5 gap-2'>
            <GraphAffaire AllAffaireData={AllAffaireData} setAllAffaireData={setAllAffaireData} />
            <div className='col-12 d-flex justify-content-between align-items-center flex-row gap-2'>
                <div className='col-6'>
                    <RendementProd AllRendementData={AllRendementData} setAllRendementData={setAllRendementData} />
                </div>
                <div className='col-6'>
                    <TRS AllTRSData={AllTRSData} setAllTRSData={setAllTRSData}/>
                </div>
            </div>
        </div>
    );
}

export default PageVueGlobale;
