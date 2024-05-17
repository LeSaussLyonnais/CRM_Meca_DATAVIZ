import React, { useEffect } from 'react';
import { Doughnut } from 'react-chartjs-2';

const RendementProd = ({ AllRendementData, setAllRendementData }) => {
    const label = ['Temps passé', 'Temps prévu restant'];

    const genereRendementData = () => {
        let rendementData = [];
        const rendementTempsPasse = Math.floor(Math.random() * 100) + 1;
        const rendementTempsRestant = Math.floor(100 - rendementTempsPasse);
        rendementData.push(rendementTempsPasse);
        rendementData.push(rendementTempsRestant);
        return rendementData;
    }

    const data = {
        labels: label,
        datasets: [
            {
                label: 'Rendement de production',
                data: AllRendementData,
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
        const rendementTempsRestant = genereRendementData();
        setAllRendementData(rendementTempsRestant);
    }

    useEffect(() => {
        setData();
    }, [])

    return (
        <div className="col-12 container-perso-content d-flex flex-column justify-content-center align-items-center px-4 py-3">
            <div className='col-12 d-flex flex-column justify-content-start align-items-start'>
                <h3 className='Title_global_1'>Rendement global de production</h3>
                <p className='Subtitle_global'>[Temps prévu / Temps passé] pour le mois en cours</p>
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

export default RendementProd;
