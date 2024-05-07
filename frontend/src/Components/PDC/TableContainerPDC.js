import React, { useEffect, useState } from 'react';
import ColorModifiedImage from '../ColorPngChange';
import tour from '../../Assets/tour.png';
import fraiseuse from '../../Assets/fraiseuse.png';
import soudure from '../../Assets/soudure.png';
import peinture from '../../Assets/peinture.png';

const TableContainerPDC = ({ PDCsemaine, semaineSelected, setPDCsemaine, setsemaineSelected }) => {
    useEffect(() => {
        initdata();
        console.log(PDCsemaine);
    }, []);

    const initdata = () => {
        setPDCsemaine(genereDataAleatoire(5, ["usinage", "soudure", "peinture"], ["soudure", "fraiseuse", "tour", "peinture"], 50, 150));
    }

    function genereDataAleatoire(nbSemaines, ateliers, typesPostes, chargesMin, chargesMax) {
        const data = [];
        for (let semaine = 1; semaine <= nbSemaines; semaine++) {
            const atelier = ateliers[Math.floor(Math.random() * ateliers.length)];
            const nbPostes = Math.floor(Math.random() * 10) + 1;
            const postes = [];
            for (let i = 0; i < nbPostes; i++) {
                postes.push({
                    poste: i + 1,
                    type: typesPostes[Math.floor(Math.random() * typesPostes.length)],
                    charge: Math.floor(Math.random() * (chargesMax - chargesMin + 1)) + chargesMin
                });
            }
            data.push({
                semaine,
                atelier,
                postes
            });
        }
        return data;
    };
  return (
    <div className='d-flex flex-column justify-content-center align-items-center container-perso-content m-3 p-3'>
                <div className='col-12 d-flex justify-content-center align-items-start flex-column'>
                    <h1 className='display-perso-4 my-2 p-2'>Plan de charge de la partie usinage</h1>
                </div>
                <hr className='text-dark px-5 w-100' />
                {PDCsemaine.length > 0 ? (
                    <div className='d-flex justify-content-center align-items-center flex-wrap gap-5'>
                        {PDCsemaine.map((semaine) => {
                            if (semaine.semaine === semaineSelected) {
                                return semaine.postes.map((poste) => (
                                    <div key={poste.poste} className='d-flex justify-content-center align-items-center flex-column m-3'>
                                        <h2 className='poste-title text-dark'>Poste : {poste.poste}</h2>
                                        <h2 className='charge-content text-dark'>Charge : {poste.charge} %</h2>
                                        <img src='' style={{ maxWidth: '100px' }} alt='' />
                                        <ColorModifiedImage imageUrl={
                                            poste.type === "tour" ? tour :
                                                poste.type === "soudure" ? soudure :
                                                    poste.type === "peinture" ? peinture :
                                                        fraiseuse
                                        } color={
                                            poste.charge < 80 ? [64, 119, 24] :
                                                poste.charge < 100 ? [246, 189, 90] :
                                                    [237, 33, 22]
                                        } />
                                    </div>
                                ));
                            } else {
                                return null; // Retourne null si ce n'est pas la première semaine
                            }
                        })}
                    </div>
                ) : (
                    <p>No weeks available.</p>
                )}
            </div>
  );
};

export default TableContainerPDC;
