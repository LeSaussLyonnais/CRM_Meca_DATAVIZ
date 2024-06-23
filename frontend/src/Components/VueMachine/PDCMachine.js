import React, { useEffect, useContext, useState, useRef } from 'react';
import { SiteContext } from '../ContexteSelectionSite';
const PDCMachine = ({ SelectedPoste, AllPDCData, setAllPDCData }) => {
  const { selectedSite, selectedWorkshop } = useContext(SiteContext);
  const socketRef = useRef(null); // Ref to store the current WebSocket connection

  const getWeekNumber = (date) => {
    const firstJan = new Date(date.getFullYear(), 0, 1);
    const pastDaysOfYear = (date - firstJan) / 86400000;
    return Math.ceil((pastDaysOfYear + firstJan.getDay() + 1) / 7);
  };

  const currentDate = new Date();
  const currentWeekNumber = getWeekNumber(currentDate);
  const currentyear = currentDate.getFullYear();

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
      const socket = new WebSocket(`ws://192.168.0.117:8000/ws/charge_machine/${SelectedPoste.COFRAIS}/${currentyear}/${currentWeekNumber}/`); //${window.location.host}

      socket.onmessage = function (event) {
        console.log('Received data:', event.data);
        setAllPDCData(JSON.parse(event.data)); // Assuming the received data is JSON
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
        const response = await fetch('http://192.168.0.117:8000/BlogApp/PDCMachine_Tache', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            nom_poste: SelectedPoste.COFRAIS,
            num_annee: currentyear,
            num_semaine: currentWeekNumber
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
          Plan de charge : {SelectedPoste.COFRAIS}
        </p>
        <p className='Subtitle_machine'>
          Liste prévisionnelle pour les 6 prochaines semaines
        </p>
        <hr className='col-12' />
      </div>

      <div className='col-12 d-flex flex-row justify-content-center align-items-start px-5 gap-3'>
        {AllPDCData.map((data, index) => {
          return (
            <div className='col d-flex flex-column justify-content-center align-items-center gap-1'>
              <div className='Text_Semaine_PDC'>
                S {data.SEMAINE}
              </div>
              <div className='rond_PDC' style={data.VDUREE <= 100 ? { backgroundColor: '#379740' } : { backgroundColor: '#CE2626' }} />
              <p className='Value_Semaine_PDC' style={data.VDUREE <= 100 ? { color: '#379740' } : { color: '#CE2626' }}>
                {data.VDUREE.toFixed(2)}h
              </p>

            </div>
          )
        })}
      </div>

    </div>
  );
};

export default PDCMachine;
