import React, { useState, useContext } from 'react';
import '../../Styles/communication.css';
import RemonterInfo from '../Communication/RemonterInfo';
import CroixSecurite from '../Communication/CroixSecurite';
import AbsenceAtelier from '../Communication/AbsenceAtelier';
import DescenteInfo from '../Communication/DescenteInfo';
import Sidebar from '../Sidebar';
import BoutonSidebar from '../BoutonSidebar';
import { SiteContext } from '../ContexteSelectionSite';

const PageCommunication = () => {
    const { selectedSite, setSelectedSite, selectedWorkshop, setSelectedWorkshop } = useContext(SiteContext);
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);

    const toggleSidebar = () => {
        setIsSidebarOpen(!isSidebarOpen);
    };

    return (
        <>
            <BoutonSidebar toggleSidebar={toggleSidebar} />
            <Sidebar isOpen={isSidebarOpen} toggleSidebar={toggleSidebar} />
            <div className="container-fluid d-flex flex-row justify-content-center align-items-center px-4 py-3 gap-2">
                <div className='col-4 d-flex flex-column justify-content-center align-items-center px-4 py-3 gap-2'>
                    <CroixSecurite />
                    <DescenteInfo />
                </div>
                <div className='col-8 d-flex flex-column justify-content-center align-items-center px-4 py-3 gap-2'>
                    <AbsenceAtelier />
                    <RemonterInfo />
                </div>
            </div>
        </>
    );
};

export default PageCommunication;
