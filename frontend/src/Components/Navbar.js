import React, { useContext, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { SlSpeedometer } from "react-icons/sl";
import { GoGear } from "react-icons/go";
import { GrStorage } from "react-icons/gr";
import { IoChatbubbleEllipsesOutline } from "react-icons/io5";
import { SiteContext } from './ContexteSelectionSite';




function Navbar() {
    const { selectedSite, setSelectedSite, selectedWorkshop, setSelectedWorkshop } = useContext(SiteContext);
    const iconSize = 40; // Taille désirée pour les icônes

    return (
        <>
            {selectedSite && selectedWorkshop &&
                <div className="navbar-container">
                    <ul className="navbar-nav justify-content-center align-items-center gap-perso">
                        <li className="nav-item">
                            <Link to="VueGlobale" className="nav-link d-flex flex-column align-items-center">
                                <SlSpeedometer size={iconSize} /> <span className="navbar-text">Vue globale</span>
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link to="/VuePoste" className="nav-link d-flex flex-column align-items-center">
                                <GoGear size={iconSize} /> <span className="navbar-text">Vue poste</span>
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link to="/PlanDeCharge" className="nav-link d-flex flex-column align-items-center">
                                <GrStorage size={iconSize} /> <span className="navbar-text">Plan de charge</span>
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link to="/Communication" className="nav-link d-flex flex-column align-items-center">
                                <IoChatbubbleEllipsesOutline size={iconSize} /> <span className="navbar-text">Communication</span>
                            </Link>
                        </li>
                    </ul>
                </div>
            }
        </>

    );
}

export default Navbar;
