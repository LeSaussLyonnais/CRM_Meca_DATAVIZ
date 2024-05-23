import React, { useState, useEffect, useContext } from 'react';
import ListOrdo from '../VuePoste/listeOrdo';
import SelectPoste from '../VuePoste/SelectPoste';
import { RendementPoste } from '../VuePoste/RendementPoste';
import PDCPoste from '../VuePoste/PDCPoste';
import { SiteContext } from '../ContexteSelectionSite';
import '../../Styles/vueposte.css'

function PageVuePoste() {
    const [SelectedPoste, setSelectedPoste] = useState({});
    const [AllPoste, setAllPoste] = useState([]);
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
                    <SelectPoste
                        SelectedPoste={SelectedPoste}
                        setSelectedPoste={setSelectedPoste}
                        AllPoste={AllPoste}
                        setAllPoste={setAllPoste}
                    />
                </div>
                <hr className='text-dark hr-custom' />

                <div className='container-perso-ordo d-flex justify-content-center align-items-center flex-row gap-4 mb-5 mt-4'>
                    <ListOrdo
                        AllOrdoFixe={AllOrdoFixe}
                        setAllOrdoFixe={setAllOrdoFixe}
                        AllOrdoVariable={AllOrdoVariable}
                        setAllOrdoVariable={setAllOrdoVariable}
                        SelectedPoste={SelectedPoste}
                    />
                    <div
                        className='col-12 col-lg-4 d-flex justify-content-between align-items-center flex-column gap-2'
                        style={{ height: '65vh' }}
                    >
                        <RendementPoste
                            AllRendementData={AllRendementData}
                            setAllRendementData={setAllRendementData}
                            SelectedPoste={SelectedPoste}
                        />
                        <PDCPoste
                            SelectedPoste={SelectedPoste}
                            AllPDCData={AllPDCData}
                            setAllPDCData={setAllPDCData}
                        />
                    </div>
                </div>
            </div>
        </>
    );
}

export default PageVuePoste;
