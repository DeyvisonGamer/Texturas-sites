Automação de Deploy

1) Ative GitHub Actions no repositório (deve estar habilitado por padrão).

2) Crie um Deploy Hook no Railway (ou use o mecanismo que preferir):
   - No painel do Railway do seu projeto, crie um "Deploy Hook" que aceite POSTs e copie a URL.

3) No GitHub, adicione um Secret chamado `RAILWAY_DEPLOY_HOOK` com a URL copiada.

4) Ao dar push no `main`, o workflow fará:
   - Build da imagem Docker e push para `ghcr.io/<owner>/<repo>/texturas-sites:...`
   - Se `RAILWAY_DEPLOY_HOOK` estiver definido, o workflow fará um POST para essa URL para disparar o deploy.

5) Observações:
   - Você também pode configurar o Railway para puxar diretamente a imagem de `ghcr.io`.
   - Se preferir outro registry (Docker Hub), é possível adaptar o workflow com credenciais.
