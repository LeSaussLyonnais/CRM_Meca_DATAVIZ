import React from 'react';
import { Link } from 'react-router-dom';
import { TfiHome } from "react-icons/tfi";
import { SlSpeedometer } from "react-icons/sl";
import { BsCardChecklist } from "react-icons/bs";
import { IoMapOutline } from "react-icons/io5";

function Navbar() {
    const iconSize = 40; // Taille désirée pour les icônes

    return (
        <div className="navbar-container">
            <ul className="navbar-nav justify-content-center align-items-center gap-perso">
                <li className="nav-item">
                    <Link to="/" className="nav-link d-flex flex-column align-items-center">
                        <TfiHome size={iconSize}/> <span className="navbar-text">Accueil</span>
                    </Link>
                </li>
                <li className="nav-item">
                    <Link to="/VueGlobale" className="nav-link d-flex flex-column align-items-center">
                        <SlSpeedometer size={iconSize}/> <span className="navbar-text">Vue globale</span>
                    </Link>
                </li>
                <li className="nav-item">
                    <Link to="/Ordonnancement" className="nav-link d-flex flex-column align-items-center">
                        <BsCardChecklist size={iconSize} /> <span className="navbar-text">Ordonnancement</span>
                    </Link>
                </li>
                <li className="nav-item">
                    <Link to="/PlanDeCharge" className="nav-link d-flex flex-column align-items-center">
                        <IoMapOutline size={iconSize}/> <span className="navbar-text">Plan de charge</span>
                    </Link>
                </li>
            </ul>
        </div>
    );
}

export default Navbar;
