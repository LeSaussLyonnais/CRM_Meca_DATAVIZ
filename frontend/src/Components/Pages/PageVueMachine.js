import React, { useState, useEffect, useContext } from 'react';
import ListOrdo from '../VueMachine/listeOrdo';
import SelectMachine from '../VueMachine/SelectMachine';
import { RendementMachine } from '../VueMachine/RendementMachine';
import PDCMachine from '../VueMachine/PDCMachine';
import { SiteContext } from '../ContexteSelectionSite';
import '../../Styles/vuemachine.css'

function PageVueMachine() {
    const [SelectedMachine, setSelectedMachine] = useState({});
    const [AllMachine, setAllMachine] = useState([]);
    const [AllOrdoFixe, setAllOrdoFixe] = useState([]);
    const [AllOrdoVariable, setAllOrdoVariable] = useState([]);
    const [AllRendementData, setAllRendementData] = useState([]);
    const [AllPDCData, setAllPDCData] = useState([]);
    const { selectedSite, setSelectedSite, selectedWorkshop, setSelectedWorkshop } = useContext(SiteContext);

    const handleSiteChange = (newSite) => {
        selectSite(newSite);
    };

    const [isActive, setIsActive] = React.useState(false);

    useEffect(() => {
        setIsActive(true);
    }, []);

    return (
        <>
            <div className={`header-ordonnancement ${isActive ? 'active' : ''}`}></div>

            <div className='container-fluid d-flex justify-content-center align-items-center flex-column'>
                <div className='col-12 px-5 m-3 d-flex justify-content-between align-items-center flex-row'>
                    <div className='col-5 d-flex justify-content-center align-items-start flex-column'>
                        <h1 className='display-perso-2 mt-0 mb-0 px-2 text-dark'>
                            Ordonnancement global de l'atelier :
                        </h1>
                    </div>
                    <SelectMachine
                        SelectedMachine={SelectedMachine}
                        setSelectedMachine={setSelectedMachine}
                        AllMachine={AllMachine}
                        setAllMachine={setAllMachine}
                    />
                </div>
                <hr className='text-dark hr-custom' />

                <div className='container-perso-ordo d-flex justify-content-center align-items-center flex-row gap-4 mb-5 mt-4'>
                    <ListOrdo
                        AllOrdoFixe={AllOrdoFixe}
                        setAllOrdoFixe={setAllOrdoFixe}
                        AllOrdoVariable={AllOrdoVariable}
                        setAllOrdoVariable={setAllOrdoVariable}
                        SelectedMachine={SelectedMachine}
                    />
                    <div
                        className='col-12 col-lg-4 d-flex justify-content-between align-items-center flex-column gap-2'
                        style={{ height: '65vh' }}
                    >
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

export default PageVueMachine;
