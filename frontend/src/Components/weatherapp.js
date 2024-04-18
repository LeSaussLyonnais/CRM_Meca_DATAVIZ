import React, { useState, useEffect } from 'react';
import '../Styles/meteo.css';

function WeatherApp() {
    // Déclaration d'un état weather pour stocker les données météorologiques
    const [weather, setWeather] = useState(null);

    useEffect(() => {
        // Effect hook pour gérer la connexion websocket
        const socket = new WebSocket(`ws://10.31.67.30:8880/ws/weather/`);

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
        <div className="container-fluid"> {/* Utilisation de container-fluid pour occuper toute la largeur */}
            <div className="row">
                <div className="col-12 mt-5"> {/* Utilisation de col-12 pour occuper toute la largeur de la grille */}
                    <h3 className="text-center mb-5">Tour conventionnel 1</h3> {/* Ajout de la classe text-center pour centrer le titre */}
                    <table id="weather-table" className="table table-hover mx-auto"> {/* Ajout de l'identifiant weather-table */}
                        <thead>
                            <tr>
                                <th scope="col">Performance machine</th>
                                <th scope="col">Indicateur</th>
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
