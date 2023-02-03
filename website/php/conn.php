

<?php
$servername = "localhost";
$username = "root";
$password = "Eric19$$";
$dbname = "music_recommendation_application";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

$conn->close();
?> 