<?php

$hf_hostname = "192.168.0.21";
$hf_port = "4900";
$hf_database = "BAC_A_SABLE";
$hf_user = "admin";
$hf_password = "Clip_SERENA";

$hf_dsn = sprintf("odbc:DRIVER={HFSQL};DNS={BAC_A_SABLE};Server Name=%s;Server Port=%s;Database=%s;UID=%s;PWD=%s;", $hf_hostname, $hf_port, $hf_database, $hf_user, $hf_password);

try {
    $dbh = new PDO($hf_dsn, $hf_user, $hf_password, [PDO::ATTR_PERSISTENT => true]);
} catch (PDOException $ex) {
    echo ($ex->getMessage());
}

try {
    $query = $dbh->prepare("SELECT * FROM CFRAIS WHERE COSECT like ?");
    $var = 'ATCRM';
    $query->execute([$var]); // Execute the query
    $result = $query->fetchAll(PDO::FETCH_ASSOC); // Fetch all rows from the result set
    var_dump($result);
} catch (PDOException $ex) {
    echo ($ex->getMessage());
}

?>