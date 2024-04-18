// Bienvenue.js
import React from "react";

function Bienvenue() {
  return (
    <>
      <div style={{ marginLeft: '2rem', marginTop: '2rem' }}> {/* Ajouter une marge à gauche */}
        <h1 className="Titre">Bonjour !</h1>
        <p className="Paragraphe">
          Bienvenue dans le Dashboard de suivi de production, veuillez selectionner le site de votre production :
        </p>
        <hr style={{marginRight: '2rem', borderTop: '1px solid black' }}/> {/* Définir une longueur spécifique pour le trait */}
      </div>
    </>
  );
}

export default Bienvenue;
