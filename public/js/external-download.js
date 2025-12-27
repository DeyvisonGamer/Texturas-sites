// public/js/external-download.js
// Coloque em /public/js/external-download.js ou equivalente
document.addEventListener('DOMContentLoaded', () => {
  const titleInput = document.getElementById('title');
  const urlInput = document.getElementById('url');
  const addBtn = document.getElementById('addBtn');
  const clearBtn = document.getElementById('clearBtn');
  const preview = document.getElementById('preview');
  const previewTitle = document.getElementById('previewTitle');
  const downloadBtn = document.getElementById('downloadBtn');
  const urlText = document.getElementById('urlText');
  const editBtn = document.getElementById('editBtn');

  function isValidUrl(s) {
    try {
      const u = new URL(s);
      return ['http:', 'https:'].includes(u.protocol);
    } catch (e) { return false; }
  }

  addBtn.addEventListener('click', async () => {
    const url = urlInput.value.trim();
    const title = titleInput.value.trim() || 'Download';
    if (!url) { alert('Informe o link de download.'); urlInput.focus(); return; }
    if (!isValidUrl(url)) {
      if (!confirm('O link parece inválido. Deseja prosseguir mesmo assim?')) return;
    }

    previewTitle.textContent = title;
    downloadBtn.href = url;
    urlText.textContent = url;
    preview.style.display = 'block';

    // Opcional: envie para o servidor para salvar meta (se existir endpoint)
    // Endpoint sugerido: POST /api/save-link
    try {
      const resp = await fetch('/api/save-link', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, url })
      });
      if (resp.ok) {
        const json = await resp.json();
        console.log('Link salvo:', json);
      } else {
        console.log('Nenhum endpoint para salvar ou ocorreu erro', resp.status);
      }
    } catch (err) {
      console.log('Erro ao enviar para /api/save-link (pode não existir):', err.message);
    }
  });

  clearBtn.addEventListener('click', () => {
    titleInput.value = '';
    urlInput.value = '';
    preview.style.display = 'none';
  });

  editBtn.addEventListener('click', () => {
    preview.style.display = 'none';
    urlInput.focus();
  });
});
