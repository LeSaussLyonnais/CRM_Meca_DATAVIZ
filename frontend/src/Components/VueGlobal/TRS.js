import React, { useEffect } from 'react';
import { Doughnut } from 'react-chartjs-2';

const TRS = ({ AllTRSData, setAllTRSData }) => {
    const label = ['Nombre de pièces conformes', 'Nombre de pièces non conformes'];

    const genereTRSData = () => {
        let TRSData = [];
        const PieceConforme = Math.floor(Math.random() * 100) + 1;
        const PieceNonConforme = Math.floor(100 - PieceConforme);
        TRSData.push(PieceConforme);
        TRSData.push(PieceNonConforme);
        return TRSData;
    }

    const data = {
        labels: label,
        datasets: [
            {
                label: 'Rendement de production',
                data: AllTRSData,
                backgroundColor: [
                    '#FDE3DF',
                    '#DB9EF0',
                ],
                borderColor: [
                    '#FDE3DF',
                    '#DB9EF0',
                ],
                borderWidth: 1,
            },
        ],
    };

    const options = {
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: true,
                position: 'right',
            },
        },
    };

    const setData = () => {
        const TRSData = genereTRSData();
        setAllTRSData(TRSData);
    }

    useEffect(() => {
        setData();
    }, [])

    return (
        <div className="col-12 container-perso-content d-flex flex-column justify-content-center align-items-center px-4 py-3">
            <div className='col-12 d-flex flex-column justify-content-start align-items-start'>
                <h3 className='Title_global_1'>TRS (Taux de Rendement Synthétique)</h3>
                <p className='Subtitle_global'>[Pièces conformes / Nombre total de pièces] pour le mois en cours</p>
                <hr className='col-12' />
            </div>
            <div
                className='col-12 d-flex flex-row justify-content-start align-items-center'
                style={{ height: '28vh' }}
            >
                <Doughnut data={data} options={options} />
            </div>
        </div>
    );
};

export default TRS;
