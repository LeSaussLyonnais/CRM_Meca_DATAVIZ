import React, { useEffect } from 'react';
import { Bar } from 'react-chartjs-2';
// import { LinearScale } from 'chart.js/auto';
import {
  CategoryScale,
  BarElement,
  LinearScale,
  Title,
  Tooltip,
  Legend,
} from 'chart.js/auto';

export function RendementMachine({ AllRendementData, setAllRendementData, SelectedMachine }) {

  const generateData = () => {
    const data = [];
    const datainf = [];
    const datasup = [];

    for (let i = 0; i < 10; i++) {
      const value = Math.floor(Math.random() * (150 - 50 + 1)) + 50;
      if (value <= 100) {
        datainf.push(100 - value);
        datasup.push(0);
        data.push(value);
      } else {
        datainf.push(0);
        datasup.push(value - 100);
        data.push(100);
      }
      var AllData = {
        data: data,
        datainf: datainf,
        datasup: datasup,
      }
    }
    // console.log(data);
    return AllData;
  }

  const labels = ['OF1', 'OF2', 'OF3', 'OF4', 'OF5', 'OF6', 'OF7', 'OF8', 'OF9', 'OF10'];

  const BarData = {
    labels,
    datasets: [
      {
        label: 'Rendement',
        data: AllRendementData.data,
        backgroundColor: '#798188',
        barThickness: 10, // Ajustez cette valeur selon vos besoins
      },
      {
        label: 'Avance Machine',
        data: AllRendementData.datainf,
        backgroundColor: '#379740',
        barThickness: 10, // Ajustez cette valeur selon vos besoins
      },
      {
        label: 'Retard Machine',
        data: AllRendementData.datasup,
        backgroundColor: '#CE2626',
        barThickness: 10, // Ajustez cette valeur selon vos besoins
      },
    ],
  };

  // Définir les plugins dans les options du graphique
  const options = {
    plugins: {
      title: {
        display: true,
      },
    },
    responsive: true,
    indexAxis: 'x', // Spécifier l'axe x comme axe d'index
    scales: {
      x: {
        stacked: true,
        grid: {
          display: false, // Désactiver le quadrillage vertical
        },
      },
      y: {
        stacked: true,
        ticks: {
          callback: function (value) {
            return value + '%'; // Ajouter le symbole de pourcentage à la fin de chaque étiquette
          }
        },
      },
    },
  };

  useEffect(() => {
    setData();
  }, []);

  useEffect(() => {
    setData();
  }, [SelectedMachine]);

  const setData = () => {
    const data = generateData();
    setAllRendementData(data);
  }

  return (
    <div className='col-12 container-perso-content d-flex flex-column justify-content-center align-items-start'>
      <div className='col-12 d-flex flex-column justify-content-center align-items-start px-5'>
        <p className='Title_machine'>
          Rendement du machine : {SelectedMachine.machine}

        </p>
        <p className='Subtitle_machine'>
          [Temps passé / temps prévu] pour les 10 derniers OF
        </p>
        <hr className='col-12' />
      </div>
      <Bar className='mx-5 mt-0 mb-5' options={options} data={BarData} />
    </div>

  );
}
