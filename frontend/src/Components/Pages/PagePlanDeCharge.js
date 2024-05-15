import React, { useEffect, useState, useContext } from 'react';
import TableContainerPDC from '../PDC/TableContainerPDC';
import SelectSemaine from '../PDC/SelectSemaine';
import { SiteContext } from '../ContexteSelectionSite';


function PagePlanDeCharge() {
    const [PDCsemaine, setPDCsemaine] = useState([]); // Ici, définissez correctement PDCsemaine
    const [semaineSelected, setsemaineSelected] = useState(12);
    const { selectedSite, setSelectedSite, selectedWorkshop, setSelectedWorkshop } = useContext(SiteContext);


    const [isActive, setIsActive] = React.useState(false);

    React.useEffect(() => {
        setIsActive(true);
    }, []);

    return (
        <>
            <div className={`header-plandecharge ${isActive ? 'active' : ''}`}>
            </div>
            <div className='container-fluid d-flex justify-content-center align-items-center flex-column'>
                <div className='col-12 px-5 m-3'>
                    <div className='col-10 col-lg-5 d-flex justify-content-center align-items-start flex-column'>
                        <h1 className='display-perso-2 mt-2 mb-0 px-2 text-dark'>Plan de charge</h1>
                        <h2 className='display-perso-4 px-2'>Indication de la charge sur la semaine sélectionnée</h2>
                    </div>
                    <SelectSemaine
                        PDCsemaine={PDCsemaine} // Assurez-vous que PDCsemaine est défini ici
                        semaineSelected={semaineSelected}
                        setPDCsemaine={setPDCsemaine}
                        setsemaineSelected={setsemaineSelected}
                    />
                    <hr className='text-dark px-5 w-100' />
                </div>
                <TableContainerPDC
                    PDCsemaine={PDCsemaine}
                    semaineSelected={semaineSelected}
                    setPDCsemaine={setPDCsemaine}
                    setsemaineSelected={setsemaineSelected}
                />
            </div>
        </>
    );
}

export default PagePlanDeCharge;
