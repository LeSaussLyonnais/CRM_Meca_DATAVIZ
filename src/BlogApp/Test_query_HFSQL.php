<?php

$hf_hostname = "192.168.0.21";
$hf_port = "4900";
$hf_database = "BAC_A_SABLE";
$hf_user = "admin";
$hf_password = "Clip_SERENA";

$hf_dsn = sprintf("odbc:DRIVER={HFSQL};DNS={BAC_A_SABLE};Server Name=%s;Server Port=%s;Database=%s;UID=%s;PWD=%s;", $hf_hostname, $hf_port, $hf_database, $hf_user, $hf_password);

try{
    $hf_dbh = new PDO($hf_dsn, $hf_user,$hf_password, [ PDO::ATTR_PERSISTENT => true]);

}
catch(PDOException $ex){
    echo($ex->getMessage());

}

?>