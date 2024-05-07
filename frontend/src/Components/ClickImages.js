// Import des bibliothèques React
import React, { useState } from 'react';
import './Styles/styles.css'; // Assurez-vous d'importer votre fichier CSS pour styliser les composants

// Définition du composant fonctionnel ClickImages
const ClickImages = () => {
  // Déclaration de l'état pour suivre quel site est agrandi
  const [siteAgrandi, setSiteAgrandi] = useState(null);

  // Fonction pour gérer le clic sur une image
  const handleClick = (site) => {
    // Si le site cliqué est déjà agrandi, le rétrécir
    if (siteAgrandi === site) {
      setSiteAgrandi(null);
    } else {
      // Sinon, agrandir le site cliqué
      setSiteAgrandi(site);
    }
  };

  return (
    <div className="click-images-container">
      {/* Image et texte du premier site */}
      <div className={`site-container ${siteAgrandi === 'site1' ? 'agrandi' : ''}`} onClick={() => handleClick('site1')}>
        <img src="chemin/vers/image1.jpg" alt="Site 1" />
        <div className="text-overlay">Texte pour le site 1</div>
      </div>

      {/* Image et texte du deuxième site */}
      <div className={`site-container ${siteAgrandi === 'site2' ? 'agrandi' : ''}`} onClick={() => handleClick('site2')}>
        <img src="chemin/vers/image2.jpg" alt="Site 2" />
        <div className="text-overlay">Texte pour le site 2</div>
      </div>

      {/* Image et texte du troisième site */}
      <div className={`site-container ${siteAgrandi === 'site3' ? 'agrandi' : ''}`} onClick={() => handleClick('site3')}>
        <img src="chemin/vers/image3.jpg" alt="Site 3" />
        <div className="text-overlay">Texte pour le site 3</div>
      </div>
    </div>
  );
};

export default ClickImages;
