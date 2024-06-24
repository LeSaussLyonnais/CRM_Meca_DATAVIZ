let urlWS;


if (window.location.href.includes("localhost")) {

  urlWS = "ws://127.0.0.1:8000/";

} else {

  urlWS = "ws://192.168.31.2:8000/";

}


export default urlWS;