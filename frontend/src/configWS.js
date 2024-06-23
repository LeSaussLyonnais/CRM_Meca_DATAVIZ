let urlWS;


if (window.location.href.includes("localhost")) {

  urlWS = "ws://localhost:8000/";

} else {

  urlWS = "ws://192.168.31.2:8000/";

}


export default urlWS;