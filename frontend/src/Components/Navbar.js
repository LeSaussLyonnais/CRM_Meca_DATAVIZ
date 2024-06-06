import React, { useContext } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { SiteContext } from './ContexteSelectionSite';
import { SlSpeedometer } from "react-icons/sl";
import { GoGear } from "react-icons/go";
import { GrStorage } from "react-icons/gr";
import { IoChatbubbleEllipsesOutline } from "react-icons/io5";
import '../Styles/header.css';

function Navbar() {
    const { selectedSite, selectedWorkshop } = useContext(SiteContext);
    const location = useLocation();
    const iconSize = 40;

    // Détermine si la navbar doit être affichée en fonction de selectedSite et selectedWorkshop
    const showNavbar = selectedSite && selectedWorkshop;

    return (
        <div className={`navbar-container ${showNavbar ? 'show' : 'hide'}`}>
            <ul className={`navbar-nav ${showNavbar ? 'show' : 'hide'}`}>
                <li className={`nav-item ${location.pathname === '/VueGlobale' ? 'active' : ''}`}>
                    <Link to="/VueGlobale" className="nav-link d-flex flex-column align-items-center">
                        <SlSpeedometer size={iconSize} /> <span className="navbar-text">Vue globale</span>
                    </Link>
                </li>
                <li className={`nav-item ${location.pathname === '/VueMachine' ? 'active' : ''}`}>
                    <Link to="/VueMachine" className="nav-link d-flex flex-column align-items-center">
                        <GoGear size={iconSize} /> <span className="navbar-text">Vue machine</span>
                    </Link>
                </li>
                <li className={`nav-item ${location.pathname === '/PlanDeCharge' ? 'active' : ''}`}>
                    <Link to="/PlanDeCharge" className="nav-link d-flex flex-column align-items-center">
                        <GrStorage size={iconSize} /> <span className="navbar-text">Plan de charge</span>
                    </Link>
                </li>
                <li className={`nav-item ${location.pathname === '/Communication' ? 'active' : ''}`}>
                    <Link to="/Communication" className="nav-link d-flex flex-column align-items-center">
                        <IoChatbubbleEllipsesOutline size={iconSize} /> <span className="navbar-text">Communication</span>
                    </Link>
                </li>
            </ul>
        </div>
    );
}

export default Navbar;
