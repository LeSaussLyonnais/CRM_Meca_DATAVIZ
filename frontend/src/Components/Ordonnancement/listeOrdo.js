import React, { useEffect } from 'react';

const ListOrdo = ({ AllOrdoFixe, setAllOrdoFixe, AllOrdoVariable, setAllOrdoVariable, SelectedMachine }) => {

    const ListOrdoHeader = [
        'Debut Ordo',
        'Client',
        'Affaire',
        'Etat',
        'Rang',
        'Temps prévu',
        'Temps écoulé',
        'Temps restant'
    ]

    const genereOrdo = (nbOrdo) => {
        const Ordo = [];
        const clients = ['Client A', 'Client B', 'Client C'];
        const affaires = ['Affaire 1', 'Affaire 2', 'Affaire 3'];
        const etats = ['En cours', 'En attente', 'Terminé'];
        const tempsPrevuMin = 1;
        const tempsPrevuMax = 10;

        for (let i = 0; i < Math.floor(Math.random() * nbOrdo); i++) {
            const debutOrdo = new Date().toLocaleDateString(); // Date actuelle
            const client = clients[Math.floor(Math.random() * clients.length)];
            const affaire = affaires[Math.floor(Math.random() * affaires.length)];
            const etat = etats[Math.floor(Math.random() * etats.length)];
            const rang = i + 1; // Numéro du rang
            const tempsPrevu = Math.floor(Math.random() * (tempsPrevuMax - tempsPrevuMin + 1)) + tempsPrevuMin;
            const tempsEcoule = Math.floor(Math.random() * tempsPrevu); // Temps écoulé aléatoire entre 0 et tempsPrevu
            const tempsRestant = tempsPrevu - tempsEcoule; // Calcul du temps restant

            Ordo.push({
                debut_Ordo: debutOrdo,
                client: client,
                affaire: affaire,
                Etat: etat,
                Rang: rang,
                temps_prevu: tempsPrevu,
                temps_ecouler: tempsEcoule,
                temps_restant: tempsRestant,
            });
        }

        return Ordo;
    };
    const SetData = () => {
        setAllOrdoFixe(genereOrdo(5));
        setAllOrdoVariable(genereOrdo(3));
    }

    useEffect(() => {
        SetData();
    }, [])

    useEffect(() => {
        SetData();
    }, [SelectedMachine])

    return (
        <div className='col-12 col-lg-6 container-perso-content d-flex flex-column justify-content-center align-items-start py-4 px-5'>
            <div className='col-12 col-lg-10 d-flex justify-content-center align-items-start flex-column'>
                <h1 className='display-perso-3 mt-2 mb-0 text-dark'>Liste d'ordonnancement</h1>
                <p className='display-perso-5 mb-0'>Liste fixe pour les 3 prochaines semaines et variable pour les 3 suivantes</p>
            </div>
            <hr className='text-dark px-5 w-100' />
            <table className='table table-hover table-perso-1 mt-4'>
                <thead className='thead-perso-1'>
                    <tr>
                        {ListOrdoHeader.map((header, index) => (
                            <th key={index}>{header}</th>

                        ))}
                    </tr>
                </thead>
                <div className='col-12 d-flex justify-content-center align-items-start flex-column mt-2'>
                    <p className='display-perso-5 mb-0'>Ordonnancement fixe</p>
                    <hr className='text-dark px-5 w-100' />
                </div>

                <tbody>
                    {AllOrdoFixe.map((ordo, index) => (
                        <tr key={index}>
                            <td>{ordo.debut_Ordo}</td>
                            <td>{ordo.client}</td>
                            <td>{ordo.affaire}</td>
                            <td>{ordo.Etat}</td>
                            <td>{ordo.Rang}</td>
                            <td>{ordo.temps_prevu}h</td>
                            <td>{ordo.temps_ecouler}h</td>
                            <td>{ordo.temps_restant}h</td>
                        </tr>
                    ))}
                </tbody>
                <div className='col-12 d-flex justify-content-center align-items-start flex-column mt-2'>
                    <p className='display-perso-5 mb-0'>Ordonnancement variable</p>
                    <hr className='text-dark px-5 w-100' />
                </div>
                <tbody>
                    {AllOrdoVariable.map((ordo, index) => (
                        <tr key={index}>
                            <td>{ordo.debut_Ordo}</td>
                            <td>{ordo.client}</td>
                            <td>{ordo.affaire}</td>
                            <td>{ordo.Etat}</td>
                            <td>{ordo.Rang}</td>
                            <td>{ordo.temps_prevu}h</td>
                            <td>{ordo.temps_ecouler}h</td>
                            <td>{ordo.temps_restant}h</td>
                        </tr>
                    ))}
                </tbody>


            </table>


        </div>
    );
};

export default ListOrdo;
