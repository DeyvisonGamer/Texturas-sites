```markdown
# Sistema de Anúncios (integração)

Arquivos adicionados:
- public/js/ads.js   -> script para admin e widget
- public/js/ads-widget.js -> script alternativo para widget
- templates/ads-admin.html -> página de administração (proteja com auth)
- api/save-ad.php    -> endpoint para salvar anúncios (PHP + PDO)
- api/get-ads.php    -> endpoint para recuperar anúncios ativos (JSON)
- sql/create_ads_table.sql -> script para criar tabela `ads`

Como usar:
1. Execute o SQL em `sql/create_ads_table.sql` no seu banco.
2. Ajuste as credenciais do banco de dados nos arquivos `api/*.php`.
3. Proteja `templates/ads-admin.html` e `api/save-ad.php` com autenticação.
4. Inclua o widget onde quiser no front-end:

<div data-ads="true" data-position="sidebar"></div>
<script src="/js/ads.js"></script>

5. Para colocar um anúncio, acesse a página admin, preencha imagem e link e salve.

Segurança e recomendações:
- Valide/limite domínios das imagens e links, e sanitize entradas no servidor.
- Use autenticação para o painel de administração.
- Evite que usuários públicos possam inserir HTML nas tags alt/urls.
- Se preferir Node/Python em vez de PHP, posso gerar a versão para sua stack.

Observações:
- O admin aqui é um exemplo simples; recomendo integrar com o sistema de login existente do seu site.
- Ao exibir anúncios, use rel="noopener noreferrer" e target="_blank" para segurança.
```
