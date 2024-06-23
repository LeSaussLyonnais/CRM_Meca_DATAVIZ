//Fichier de gestion de l'url de fetch

let urlAPI;


if (window.location.href.includes("localhost")) {

  urlAPI = "http://localhost:8000/";

} else {

  urlAPI = "http://192.168.31.2:8000/";

}


export default urlAPI;