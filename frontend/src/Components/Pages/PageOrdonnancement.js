// PageOrdonnancement.js
import React, { useState, useEffect } from 'react';
import ListOrdo from '../Ordonnancement/listeOrdo';
import SelectMachine from '../Ordonnancement/selectMachine';
import { RendementMachine } from '../Ordonnancement/RendementMachine';
import PDCMachine from '../Ordonnancement/PDCMachine'; import FullWidthTabs from '../BarreSites';
import { useSiteSelection } from '../SiteSelectionContext';

function PageOrdonnancement() {
    const [selectedSite, selectSite] = useState(useSiteSelection());
    const [SelectedMachine, setSelectedMachine] = useState({});
    const [AllMachine, setAllMachine] = useState([]);
    const [AllOrdoFixe, setAllOrdoFixe] = useState([]);
    const [AllOrdoVariable, setAllOrdoVariable] = useState([]);
    const [AllRendementData, setAllRendementData] = useState([]);
    const [AllPDCData, setAllPDCData] = useState([]);

    const handleSiteChange = (newSite) => {
        selectSite(newSite);
    };

    const [isActive, setIsActive] = React.useState(false);

    React.useEffect(() => {
        setIsActive(true);
    }, []);

    return (<>
        <div className={`header-ordonnancement ${isActive ? 'active' : ''}`}>
            <FullWidthTabs selectedSite={selectedSite} onSiteChange={handleSiteChange} />
        </div>

        <div className='container-fluid d-flex justify-content-center align-items-center flex-column'>
            <div className='col-12 px-5 m-3'>
                <div className='col-10 col-lg-5 d-flex justify-content-center align-items-start flex-column'>
                    <h1 className='display-perso-2 mt-2 mb-0 px-2 text-dark'>Ordonnacement </h1>
                </div>
                <SelectMachine
                    SelectedMachine={SelectedMachine}
                    setSelectedMachine={setSelectedMachine}
                    AllMachine={AllMachine}
                    setAllMachine={setAllMachine}
                />
                <hr className='text-dark px-5 w-100' />

            </div>
            <div className='container-perso-ordo d-flex justify-content-center align-items-center flex-row gap-4 mb-5'>
                <ListOrdo
                    AllOrdoFixe={AllOrdoFixe}
                    setAllOrdoFixe={setAllOrdoFixe}
                    AllOrdoVariable={AllOrdoVariable}
                    setAllOrdoVariable={setAllOrdoVariable}
                    SelectedMachine={SelectedMachine}
                />
                <div className='col-12 col-lg-4 d-flex justify-content-center align-items-center flex-column gap-2' style={{height: '70vh'}}>
                    <RendementMachine
                        AllRendementData={AllRendementData}
                        setAllRendementData={setAllRendementData}
                        SelectedMachine={SelectedMachine}
                    />
                    <PDCMachine
                        SelectedMachine={SelectedMachine}
                        AllPDCData={AllPDCData} 
                        setAllPDCData={setAllPDCData}
                    />
                </div>
            </div>
        </div>
    </>
    );
}

export default PageOrdonnancement;
