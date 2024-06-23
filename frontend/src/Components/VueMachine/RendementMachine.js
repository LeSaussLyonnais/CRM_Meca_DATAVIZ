import React, { useEffect, useContext, useState, useRef } from 'react';
import { Bar } from 'react-chartjs-2';
import { SiteContext } from '../ContexteSelectionSite';

// import { LinearScale } from 'chart.js/auto';
import {
  CategoryScale,
  BarElement,
  LinearScale,
  Title,
  Tooltip,
  Legend,
} from 'chart.js/auto';

export function RendementMachine({ AllRendementData, setAllRendementData, SelectedPoste }) {


  const generateData = () => {

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
      const socket = new WebSocket(`ws://192.168.0.117:8000/ws/last10of/${SelectedPoste.COFRAIS}/`); //${window.location.host}

      socket.onmessage = function (event) {
        console.log('Received data:', event.data);
        let tempdata = JSON.parse(event.data);
        let data = [];
        let datainf = [];
        let datasup = [];
        console.log(tempdata);
        tempdata.map(of => {
          if (of.VAL_FINALE >= 0) {
            datasup.push(of.VAL_FINALE);
            datainf.push(0);
            data.push(100);
          }
          else {
            datasup.push(0);
            datainf.push(Math.abs(of.VAL_FINALE));
            data.push(100 - Math.abs(of.VAL_FINALE));
          }
        })
        let AllData = {
          data: data,
          datainf: datainf,
          datasup: datasup,
        };
        setAllRendementData(AllData); // Assuming the received data is JSON
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
        const response = await fetch('http://192.168.0.117:8000/BlogApp/Last10OF_Tache', {
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

  return (
    <div className='col-12 container-perso-content d-flex flex-column justify-content-center align-items-start'>
      <div className='col-12 d-flex flex-column justify-content-center align-items-start px-5'>
        <p className='Title_machine'>
          Rendement du machine : {SelectedPoste.COFRAIS}

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
