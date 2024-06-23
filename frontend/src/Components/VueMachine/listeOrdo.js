import React, { useEffect, useContext, useState, useRef } from 'react';
import { SiteContext } from '../ContexteSelectionSite';


const ListOrdo = ({ AllOrdoVariable, setAllOrdoVariable, SelectedPoste }) => {

    const ListOrdoHeader = [
        'Debut Ordo',
        'Client',
        'Affaire',
        'Etat',
        'Rang',
        'Pièce mère',
        'Phase',
        'Phase Precedente',
        'Phase Suivante',
        'Qté restante',
        'Temps prévu',
        'Temps écoulé'
    ]

    // const genereOrdo = (nbOrdo) => {
    //     const Ordo = [];
    //     const clients = ['Client A', 'Client B', 'Client C'];
    //     const affaires = ['Affaire 1', 'Affaire 2', 'Affaire 3'];
    //     const etats = ['F', 'I', 'C'];
    //     const tempsPrevuMin = 1;
    //     const tempsPrevuMax = 10;

    //     const nbMinOrdo = 4;
    //     for (let i = 0; i < Math.floor(Math.random() * (nbOrdo - nbMinOrdo) + nbMinOrdo); i++) {
    //         //genere moi une date passé aléatoire
    //         const date = new Date();
    //         date.setDate(date.getDate() - Math.floor(Math.random() * 30));
    //         const debutOrdo = date.toLocaleDateString(); // Date actuelle
    //         const client = clients[Math.floor(Math.random() * clients.length)];
    //         const affaire = affaires[Math.floor(Math.random() * affaires.length)];
    //         const etat = etats[Math.floor(Math.random() * etats.length)];
    //         const rang = i + 1; // Numéro du rang
    //         const qteRestante = Math.floor(Math.random() * 10) + 1; // Quantité restante avec un numéro aléatoire
    //         const phase = Math.floor(Math.random() * 10); // Phase avec un numéro aléatoire
    //         const pieceMere = 'XXXXXX' + (i + 1); // Piece mère avec un numéro aléatoire
    //         const tempsPrevu = Math.floor(Math.random() * (tempsPrevuMax - tempsPrevuMin + 1)) + tempsPrevuMin;
    //         const tempsEcoule = Math.floor(Math.random() * tempsPrevu); // Temps écoulé aléatoire entre 0 et tempsPrevu

    //         Ordo.push({
    //             debut_Ordo: debutOrdo,
    //             client: client,
    //             affaire: affaire,
    //             Etat: etat,
    //             Rang: rang,
    //             Piece_Mere: pieceMere,
    //             Phase: phase,
    //             Qté_restante: qteRestante,
    //             temps_prevu: tempsPrevu,
    //             temps_ecouler: tempsEcoule,
    //         });
    //     }

    //     return Ordo;
    // };
    // const SetData = () => {
    //     setAllOrdoFixe(genereOrdo(5));
    //     setAllOrdoVariable(genereOrdo(3));
    // }

    // useEffect(() => {
    //     SetData();
    // }, [])

    // useEffect(() => {
    //     SetData();
    // }, [SelectedMachine])

    //////////////////////////////////////////////////////
    //////////////////////////////////////////////////////
    const [AllOrdoFixe, setAllOrdoFixe] = useState([]);
    const { selectedSite, selectedWorkshop } = useContext(SiteContext);
    const socketRef = useRef(null); // Ref to store the current WebSocket connection

    useEffect(() => {

        const setupWebSocket = () => {
            if (!selectedSite || !selectedWorkshop || !SelectedPoste.COFRAIS) { 
                console.error("selectedSite, selectedWorkshop, or SelectedPoste is null or SelectedPoste.COFRAIS is undefined");
                return;
            } //|| !SelectedPoste || !SelectedPoste.COFRAIS

            // Clean up the previous WebSocket connection if exists
            if (socketRef.current) {
                socketRef.current.close();
            }

            // Effect hook pour gérer la connexion websocket
            const socket = new WebSocket(`ws://192.168.0.117:8000/ws/ordo/${SelectedPoste.COFRAIS}/`); //${window.location.host}

            socket.onmessage = function (event) {
                console.log('Received data:', event.data);
                setAllOrdoFixe(JSON.parse(event.data)); // Assuming the received data is JSON
            }

            socket.onclose = function (event) {
                console.log('WebSocket closed:', event);
            }

            socket.onerror = function (error) {
                console.error('WebSocket error:', error);
            }

            socketRef.current = socket;
        }

        const UpdateFetch = async () => {
            if (!selectedSite || !selectedWorkshop || !SelectedPoste.COFRAIS) {
                console.error("selectedSite, selectedWorkshop, or SelectedPoste is null or SelectedPoste.COFRAIS is undefined");
                return;
            }

            try {
                const response = await fetch('http://192.168.0.117:8000/BlogApp/Ordo_Poste_Tache', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        nom_poste: SelectedPoste.COFRAIS,
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

        if (SelectedPoste && selectedSite && selectedWorkshop) {
            UpdateFetch();
            setupWebSocket();
        }
    }, [SelectedPoste]);

    // Cleanup WebSocket connection when the component unmounts
    useEffect(() => {
        return () => {
            if (socketRef.current) {
                socketRef.current.close();
            }
        }
    }, []);
    //////////////////////////////////////////////////////
    //////////////////////////////////////////////////////


    return (
        <div
            className='col-12 col-lg-8 container-perso-content d-flex flex-column justify-content-start align-items-start pb-4 px-5 overflow-auto'
            style={{ height: '65vh' }}
        >
            <div className='col-12 col-lg-10 d-flex justify-content-center align-items-start flex-column'>
                <h1 className='Title_machine'>Liste d'ordonnancement</h1>
                <p className='Subtitle_machine'>Liste fixe pour les 3 prochaines semaines et variable pour les 3 suivantes</p>
            </div>
            <hr className='text-dark px-5 w-100' />
            <table className='table table-hover table-perso-1'>
                <thead className='thead-perso-1 '>
                    <tr className='text-center'>
                        {ListOrdoHeader.map((header, index) => (
                            header === "Debut Ordo" ?
                                <th key={index} className='text-start'>{header}</th>
                                :
                                <th key={index}>{header}</th>
                        ))}
                    </tr>
                </thead>

                <tbody>
                    {AllOrdoFixe.map((ordo, index) => (
                        <tr key={ordo.GACLEUNIK} className='text-center'>
                            <td className='text-start'>{ordo.DATE_ORDO}</td>
                            <td>{ordo.CLIENT_NOM}</td>
                            <td>{ordo.NAF}</td>
                            <td>{ordo.ETATAF}</td>
                            <td>{ordo.RANG}</td>
                            <td>{ordo.EN_PIECE}</td>
                            <td>{ordo.PHASE}</td>
                            <td>{ordo.PHASE_AVANT}</td>
                            <td>{ordo.PHASE_SUIVANTE}</td>
                            <td>{ordo.QTEAF}</td>
                            <td>{ordo.TOTAL_TEMPS}h</td>
                            <td>{ordo.GA_NBHR}h</td>
                        </tr>
                    ))}
                </tbody>
                {/* <div className='col-12 d-flex justify-content-center align-items-start flex-column mt-2 ps-2'>
                    <p className='display-perso-5 mb-0'>Ordonnancement variable</p>
                    <hr className='text-dark px-5 w-100' />
                </div>
                <tbody>
                    {AllOrdoVariable.map((ordo, index) => (
                        <tr key={index} className='text-center'>
                            <td className='text-start'>{ordo.debut_Ordo}</td>
                            <td>{ordo.client}</td>
                            <td>{ordo.affaire}</td>
                            <td>{ordo.Etat}</td>
                            <td>{ordo.Rang}</td>
                            <td>{ordo.Piece_Mere}</td>
                            <td>{ordo.Phase}</td>
                            <td>{ordo.Qté_restante}</td>
                            <td>{ordo.temps_prevu}h</td>
                            <td>{ordo.temps_ecouler}h</td>
                        </tr>
                    ))}
                </tbody> */}


            </table>


        </div>
    );
};

export default ListOrdo;
