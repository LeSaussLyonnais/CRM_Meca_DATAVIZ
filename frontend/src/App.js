/*
import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
*/
import React, { useState, useEffect } from 'react';

function WeatherApp() {
    // Déclaration d'un état weather pour stocker les données météorologiques
    const [weather, setWeather] = useState(null);

    useEffect(() => {
        // Effect hook pour gérer la connexion websocket
        const socket = new WebSocket(`ws://${window.location.host}/ws/weather/`);

        // Fonction de rappel appelée lors de la réception de messages websocket
        socket.onmessage = function(event) {
            // Mise à jour de l'état weather avec les données reçues du websocket
            setWeather(JSON.parse(event.data));
        }

        // Nettoyage de la connexion websocket lors du démontage du composant
        return () => {
            socket.close();
        };
    }, []); // Les crochets vides en tant que dépendance indiquent que cet effet ne doit être exécuté qu'une seule fois après le montage initial du composant

    return (
        <div className="container">
            <div className="row">
                <div className="col-6 mx-auto mt-5">
                    <h3 className="mb-5">Weather in Tolosa</h3>
                    <table className="table table-hover">
                        <thead>
                            <tr>
                                <th scope="col">Temperature</th>
                                <th scope="col">Icon</th>
                                <th scope="col">Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            {/* Rendu conditionnel des données météorologiques */}
                            {weather && weather.map(wthr => (
                                <tr key={wthr.id}>
                                    <td className={`align-middle ${wthr.state === 'raise' ? 'raise' : 'fall'}`}>
                                        {wthr.temp}
                                    </td>
                                    <td className="align-middle">
                                        <img src={`https://openweathermap.org/img/wn/${wthr.icon}@2x.png`}
                                            alt=""
                                            className="px-2"
                                        />
                                    </td>
                                    <td className="align-middle">{wthr.dt_txt}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}

export default WeatherApp;

