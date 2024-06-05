import React, { useEffect, useContext, useState } from 'react';
import ColorModifiedImage from '../ColorPngChange';
import tour from '../../Assets/tour.png';
import fraiseuse from '../../Assets/fraiseuse.png';
import soudure from '../../Assets/soudure.png';
import peinture from '../../Assets/peinture.png';
import { SiteContext } from '../ContexteSelectionSite';

const TableContainerPDC = ({ semaineSelected }) => {
    const [PDCsemaine, setPDCsemaine] = useState([]);
    const annee = '2024';
    const { selectedSite, selectedWorkshop } = useContext(SiteContext);

    useEffect(() => {
        const fetchData = async () => {
            if (!selectedSite || !selectedWorkshop) {
                console.error("selectedSite or selectedWorkshop is null");
                return;
            }

            const socket = new WebSocket(`ws://127.0.0.1:8000/ws/charge/${selectedSite.COSECT}/${selectedWorkshop.Libelle_Atelier}/${annee}/${semaineSelected}/`);

            socket.onmessage = function (event) {
                console.log('Received data:', event.data);
                const parsedData = JSON.parse(event.data);
                setPDCsemaine(parsedData);
            };

            socket.onopen = () => {
                console.log('WebSocket connected');
            };

            socket.onerror = (error) => {
                console.error('WebSocket Error: ', error);
            };

            return () => {
                socket.close();
            };
        };

        const UpdateFetch = async () => {
            if (!selectedSite || !selectedWorkshop) {
                console.error("selectedSite or selectedWorkshop is null");
                return;
            }

            try {
                const response = await fetch('http://127.0.0.1:8000/BlogApp/PDC_Atelier_Tache', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        nom_site: selectedSite.COSECT,
                        nom_atelier: selectedWorkshop.Libelle_Atelier,
                        num_annee: annee,
                        num_semaine: semaineSelected,
                    }),
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const data = await response.json();
                console.log('UpdateFetch response data:', data);

            } catch (error) {
                console.error('Error:', error);
            }
        };

        if (semaineSelected && selectedSite && selectedWorkshop) {
            UpdateFetch();
            fetchData();
        }
    }, [semaineSelected, selectedSite, selectedWorkshop]);

    return (
        <div className='d-flex flex-column justify-content-center align-items-center container-perso-content m-3 p-3'>
            <div className='col-12 d-flex justify-content-center align-items-start flex-column'>
                <h1 className='display-perso-4 my-2 p-2'>Plan de charge de la partie usinage</h1>
            </div>
            <hr className='text-dark px-5 w-100' />
            {PDCsemaine.length > 0 ? (
                <div className='d-flex justify-content-center align-items-center flex-wrap gap-5'>
                    {PDCsemaine.map((Poste, index) => (
                        Poste.SEMAINE === semaineSelected && (
                            <div key={Poste.COFRAIS} className='d-flex justify-content-center align-items-center flex-column m-3'>
                                <h2 className='poste-title text-dark'>Poste : {Poste.COFRAIS}</h2>
                                <h2 className='charge-content text-dark'>Charge : {Poste.VDUREE} %</h2>
                                <ColorModifiedImage imageUrl={
                                    Poste.COFRAIS.includes("TOUR") ? tour :
                                    Poste.COFRAIS.includes("SOUDURE") ? soudure :
                                    Poste.COFRAIS.includes("PEINTURE") ? peinture :
                                    fraiseuse
                                } color={
                                    Poste.VDUREE < 80 ? [64, 119, 24] :
                                    Poste.VDUREE < 100 ? [246, 189, 90] :
                                    [237, 33, 22]
                                } />
                            </div>
                        )
                    ))}
                </div>
            ) : (
                <p>No data for this week.</p>
            )}
        </div>
    );
};

export default TableContainerPDC;
