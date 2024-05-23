import React, { useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';

const GraphAffaire = ({ AllAffaireData, setAllAffaireData }) => {
    const label = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'];

    const data = {
        labels: label,
        datasets: [
            {
                label: 'Nombre d\'affaires livrées',
                data: AllAffaireData, // Exemple de données
                fill: false,
                backgroundColor: 'rgba(219, 158, 240, 0.8)', // Couleur de fond avec transparence
                borderColor: '#DB9EF0',
                borderWidth: 1, // Épaisseur de la bordure
                tension: 0
            }
        ]
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                min: 0,
                max: 120,
                ticks: {
                    font: {
                        size: 12, // Taille de police
                        family: 'Poppins', // Police de caractère
                        weight: '500', // Poids de police
                        style: 'normal' // Style de police
                    },
                    color: '#999999', // Couleur de texte
                },
            },
            x: {
                grid: {
                    display: false, // Pour enlever le quadrillage vertical
                },
                ticks: {
                    font: {
                        size: 12, // Taille de police
                        family: 'Poppins', // Police de caractère
                        weight: '500', // Poids de police
                        style: 'normal' // Style de police
                    },
                    color: '#999999', // Couleur de texte
                }
            }
        },
        plugins: {
            legend: {
                display: false,
            }
        }
    };

    const generateData = () => {
        let temp_data = [];
        const mindata = 50;
        const maxdata = 100;
        for (let i = 0; i < label.length; i++) {
            temp_data.push(Math.floor(Math.random() * (maxdata - mindata) + mindata));
        }
        return temp_data;
    };

    const setdata = () => {
        setAllAffaireData(generateData());
    };

    useEffect(() => {
        setdata();
    }, []);

    return (
        <div
            className="col-12 container-perso-content d-flex flex-column justify-content-center align-items-center px-4 py-3"
            style={{ height: '35vh' }}
        >
            <div className='col-12 d-flex flex-column justify-content-between align-items-center'>
                <div className='col-12 d-flex flex-row justify-content-between align-items-center'>
                    <div className='d-flex flex-column justify-content-center align-items-start'>
                        <h3 className='Title_global_1'>Affaires livrées</h3>
                        <p className='Subtitle_global'>Pour les 12 derniers mois</p>
                    </div>
                    <h3 className='Title_global_2'>Affaires totales livrées : X</h3>
                </div>
                <hr className='col-12' />
            </div>
            <div
                className='col-12 d-flex flex-row justify-content-center align-items-center'
                style={{ height: '23vh' }}
            >
                <Line data={data} options={options} />
            </div>
        </div>
    );
};

export default GraphAffaire;
