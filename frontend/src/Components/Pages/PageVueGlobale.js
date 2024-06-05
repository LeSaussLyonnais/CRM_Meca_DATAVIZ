import React, { useState, useEffect, useContext } from 'react';
import { SiteContext } from '../ContexteSelectionSite';
import GraphAffaire from '../VueGlobal/GraphAffaire';
import TRS from '../VueGlobal/TRS';
import RendementProd from '../VueGlobal/RendementProd';
import Sidebar from '../Sidebar';
import BoutonSidebar from '../BoutonSidebar';
import '../../Styles/vueglobale.css';

function PageVueGlobale() {
    const { selectedSite, setSelectedSite, selectedWorkshop, setSelectedWorkshop } = useContext(SiteContext);
    const [AllAffaireData, setAllAffaireData] = useState([]);
    const [AllRendementData, setAllRendementData] = useState([]);
    const [AllTRSData, setAllTRSData] = useState([]);
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);

    const toggleSidebar = () => {
        setIsSidebarOpen(!isSidebarOpen);
    };

    return (
        <div className='page-container'>
            <BoutonSidebar toggleSidebar={toggleSidebar} />
            <Sidebar isOpen={isSidebarOpen} toggleSidebar={toggleSidebar} />
            <div className='container-fluid d-flex justify-content-center align-items-center flex-column mb-5 mt-4 px-5 gap-2'>
                <GraphAffaire AllAffaireData={AllAffaireData} setAllAffaireData={setAllAffaireData} />
                <div className='col-12 d-flex justify-content-between align-items-center flex-row gap-2'>
                    <div className='taille-camemberts'>
                        <RendementProd AllRendementData={AllRendementData} setAllRendementData={setAllRendementData} />
                    </div>
                    <div className='taille-camemberts'>
                        <TRS AllTRSData={AllTRSData} setAllTRSData={setAllTRSData}/>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default PageVueGlobale;
