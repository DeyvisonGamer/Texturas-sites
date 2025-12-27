<?php
// api/save-link.php
// Exemplo: api/save-link.php
// Ajuste: configurar conexão, permissões e validações conforme sua aplicação.

header('Content-Type: application/json');

$input = json_decode(file_get_contents('php://input'), true);
if (!$input || empty($input['url'])) {
  http_response_code(400);
  echo json_encode(['error' => 'URL é obrigatória']);
  exit;
}

$title = isset($input['title']) ? trim($input['title']) : null;
$url = trim($input['url']);

// Validação simples
if (!filter_var($url, FILTER_VALIDATE_URL)) {
  // Ainda assim aceitamos, mas podia rejeitar:
  // http_response_code(400); echo json_encode(['error'=>'URL inválida']); exit;
}

// Conexão MySQL (exemplo PDO)
$host = '127.0.0.1';
$db   = 'seu_banco';
$user = 'seu_usuario';
$pass = 'sua_senha';
$charset = 'utf8mb4';

$dsn = "mysql:host=$host;dbname=$db;charset=$charset";
$options = [ PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC ];

try {
  $pdo = new PDO($dsn, $user, $pass, $options);
  $stmt = $pdo->prepare('INSERT INTO textures (title, external_url, created_at) VALUES (:title, :url, NOW())');
  $stmt->execute([':title' => $title, ':url' => $url]);
  echo json_encode(['ok' => true, 'id' => $pdo->lastInsertId()]);
} catch (Exception $e) {
  http_response_code(500);
  echo json_encode(['error' => 'Erro ao salvar: ' . $e->getMessage()]);
}
