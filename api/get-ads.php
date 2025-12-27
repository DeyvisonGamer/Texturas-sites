<?php
// api/get-ads.php
// Retorna anúncios ativos (JSON). Parâmetro opcional: ?position=sidebar
header('Content-Type: application/json');
$position = isset($_GET['position']) ? trim($_GET['position']) : '';

// Configurar conforme seu ambiente: ajuste host/db/user/password
$host = '127.0.0.1';
$db   = 'seu_banco';
$user = 'seu_usuario';
$pass = 'sua_senha';
$charset = 'utf8mb4';
$dsn = "mysql:host=$host;dbname=$db;charset=$charset";
$options = [ PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC ];

try {
  $pdo = new PDO($dsn, $user, $pass, $options);
  if ($position !== '') {
    $stmt = $pdo->prepare('SELECT id, image_url, target_url, alt, position FROM ads WHERE active=1 AND position = :pos ORDER BY id DESC');
    $stmt->execute([':pos'=>$position]);
  } else {
    $stmt = $pdo->query('SELECT id, image_url, target_url, alt, position FROM ads WHERE active=1 ORDER BY id DESC');
  }
  $rows = $stmt->fetchAll();
  echo json_encode($rows);
} catch (Exception $e) {
  http_response_code(500);
  echo json_encode(['error'=>'Erro ao buscar anúncios: '. $e->getMessage()]);
}
?>
