//Fichier de gestion de l'url de fetch

let urlAPI;


if (window.location.href.includes("localhost")) {

  urlAPI = "http://127.0.0.1:8000/";

} else {

  urlAPI = "http://192.168.31.2:8000/";

}


export default urlAPI;