# Tenma Textures — Painel e site

Projeto mínimo para hospedar e gerenciar uma textura Minecraft chamada "Tenma".

Funcionalidades:
- Página pública com botão de download (.zip)
- Área admin com login (usuario: `tenma`, senha: `deyvison`)
- Upload de .zip pelo painel admin
- Registro de versões em `data/versions.json`
- Seção de sugestões (anônimas) armazenadas em `data/suggestions.json`

Executar localmente:

```bash
# instalar dependências
python3 -m pip install -r requirements.txt

# iniciar
python3 app.py

# abrir no navegador: http://localhost:5000
```

Admin:
- URL: http://localhost:5000/admin
- Usuário: `tenma`
- Senha: `deyvison`

Observações para Github:
- Este projeto é um app Flask; GitHub Pages não executa Flask. Para hospedar grátis, use Render, Railway ou templates de GitHub Actions + um serviço de container.

Licença e Copyright
- © Tenma Textures — Deyvison (cofundador & desenvolvedor) & Tenma (fundador & design) — desde 2025
# Texturas-sites