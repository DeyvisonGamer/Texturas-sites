<?php
// api/save-ad.php
// Salva um anúncio na tabela `ads`.
// IMPORTANTE: proteja este endpoint (autenticação) antes de usar em produção.

header('Content-Type: application/json');
$raw = file_get_contents('php://input');
$data = json_decode($raw, true);
if (!$data) { http_response_code(400); echo json_encode(['error'=>'JSON inválido']); exit; }

$image_url = isset($data['image_url']) ? trim($data['image_url']) : null;
$target_url = isset($data['target_url']) ? trim($data['target_url']) : null;
$alt = isset($data['alt']) ? trim($data['alt']) : null;
$position = isset($data['position']) ? trim($data['position']) : null;
$active = isset($data['active']) ? (int)$data['active'] : 1;

if (!$image_url || !$target_url) { http_response_code(400); echo json_encode(['error'=>'image_url e target_url são obrigatórios']); exit; }

// Validação simples de URL (opcionalmente rejeitar URLs inválidas)
if (!filter_var($image_url, FILTER_VALIDATE_URL) || !filter_var($target_url, FILTER_VALIDATE_URL)) {
  // Recomendado: retornar erro. Por enquanto, apenas logamos.
  // http_response_code(400); echo json_encode(['error'=>'URL inválida']); exit;
}

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
  $stmt = $pdo->prepare('INSERT INTO ads (image_url, target_url, alt, position, active, created_at) VALUES (:image, :target, :alt, :position, :active, NOW())');
  $stmt->execute([':image'=>$image_url, ':target'=>$target_url, ':alt'=>$alt, ':position'=>$position, ':active'=>$active]);
  echo json_encode(['ok'=>true,'id'=>$pdo->lastInsertId()]);
} catch (Exception $e) {
  http_response_code(500);
  echo json_encode(['error'=>'Erro ao salvar: '. $e->getMessage()]);
}
?>
