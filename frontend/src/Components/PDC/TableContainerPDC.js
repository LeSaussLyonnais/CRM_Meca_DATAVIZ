import React, { useEffect, useState, useContext } from 'react';
import ColorModifiedImage from '../ColorPngChange';
import tour from '../../Assets/tour.png';
import fraiseuse from '../../Assets/fraiseuse.png';
import soudure from '../../Assets/soudure.png';
import peinture from '../../Assets/peinture.png';
import SelectSemaine from './SelectSemaine';
import { SiteContext } from '../ContexteSelectionSite';

const TableContainerPDC = ({ PDCsemaine, semaineSelected, setPDCsemaine, setsemaineSelected }) => {

    let annee = '2024'

    const { selectedSite, setSelectedSite, selectedWorkshop, setSelectedWorkshop } = useContext(SiteContext);
    const socketRef = useRef(null); // Ref to store the current WebSocket connection

    useEffect(() => {
        if (semaineSelected){
            UpdateFetch()
            fetchData()
        }
        console.log(PDCsemaine);
    }, []);

    useEffect(() => {
        if (semaineSelected) {
            UpdateFetch();
            setupWebSocket();
        }
    }, [semaineSelected]);

    // const initdata = () => {
    //     setPDCsemaine(genereDataAleatoire(5, ["usinage", "soudure", "peinture"], ["soudure", "fraiseuse", "tour", "peinture"], 50, 150));
    // }

    // function genereDataAleatoire(nbSemaines, ateliers, typesPostes, chargesMin, chargesMax) {
    //     const data = [];
    //     for (let semaine = 1; semaine <= nbSemaines; semaine++) {
    //         const atelier = ateliers[Math.floor(Math.random() * ateliers.length)];
    //         const nbPostes = Math.floor(Math.random() * 10) + 1;
    //         const postes = [];
    //         for (let i = 0; i < nbPostes; i++) {
    //             postes.push({
    //                 poste: i + 1,
    //                 type: typesPostes[Math.floor(Math.random() * typesPostes.length)],
    //                 charge: Math.floor(Math.random() * (chargesMax - chargesMin + 1)) + chargesMin
    //             });
    //         }
    //         data.push({
    //             semaine,
    //             atelier,
    //             postes
    //         });
    //     }
    //     return data;
    // };

    const setupWebSocket = () => {
        // Clean up the previous WebSocket connection if exists
        if (socketRef.current) {
            socketRef.current.close();
        }

        // Effect hook pour gérer la connexion websocket
        const socket = new WebSocket(`ws://127.0.0.1:8000/ws/charge/${selectedSite.COSECT}/${selectedWorkshop.Libelle_Atelier}/${annee}/${semaineSelected}/`); //${window.location.host}

        socket.onmessage = function (event) {
            console.log('Received data:', event.data);
            setPDCsemaine(JSON.parse(event.data)); // Assuming the received data is JSON
        }

        socket.onclose = function (event) {
            console.log('WebSocket closed:', event);
        }

        socket.onerror = function (error) {
            console.error('WebSocket error:', error);
        }

        socketRef.current = socket;
    }

    // Cleanup WebSocket connection when the component unmounts
    useEffect(() => {
        return () => {
            if (socketRef.current) {
                socketRef.current.close();
            }
        }
    }, []);

    const UpdateFetch = async () => {
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

            const data = await response.json();
            console.log(data);

        } catch (error) {
            console.error('Error:', error);
        }
    }

    return (
        <div className='d-flex flex-column justify-content-center align-items-center container-perso-content m-3 p-3'>
            <div className='col-12 d-flex justify-content-center align-items-start flex-column'>
                <h1 className='display-perso-4 my-2 p-2'>Plan de charge de la partie usinage</h1>
            </div>
            <hr className='text-dark px-5 w-100' />
            {(PDCsemaine && PDCsemaine?.Charge && PDCsemaine.Charge.length > 0) ? (
                <div className='d-flex justify-content-center align-items-center flex-wrap gap-5'>
                    {PDCsemaine?.Charge.map((Poste, index) => {
                        if (Poste.SEMAINE === semaineSelected) {
                            return (
                                <div key={Poste.COFRAIS} className='d-flex justify-content-center align-items-center flex-column m-3'>
                                    <h2 className='poste-title text-dark'>Poste : {Poste.Poste_ID}</h2>
                                    <h2 className='charge-content text-dark'>Charge : {Poste.VDUREE} %</h2>
                                    <img src='' style={{ maxWidth: '100px' }} alt='' />
                                    <ColorModifiedImage imageUrl={
                                        PDCsemaine.Poste_ids[index].DESIGN.includes("TOUR") ? tour :
                                            PDCsemaine.Poste_ids[index].DESIGN.includes("SOUDURE") ? soudure :
                                                PDCsemaine.Poste_ids[index].DESIGN.includes("PEINTURE") ? peinture :
                                                    fraiseuse
                                    } color={
                                        Poste.VDUREE < 80 ? [64, 119, 24] :
                                            Poste.VDUREE < 100 ? [246, 189, 90] :
                                                [237, 33, 22]
                                    } />
                                </div>
                            );
                        } else {
                            return null;
                        }
                    })}
                </div>
            ) : (
                <p>No data for this weeks.</p>
            )}
        </div>
    );
};

export default TableContainerPDC;
