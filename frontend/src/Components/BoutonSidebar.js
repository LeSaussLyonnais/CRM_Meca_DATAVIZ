import React from 'react';
import boutonsidebar from '../Assets/boutonsidebar.png';
import '../Styles/boutonsidebar.css';

function BoutonSidebar({ toggleSidebar }) {
    return (
        <button className="bouton-sidebar" onClick={toggleSidebar}>
            <img src={boutonsidebar} alt="Toggle Sidebar" />
        </button>
    );
}

export default BoutonSidebar;
