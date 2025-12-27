// public/js/ads.js
// Script para painel admin (salvar anúncios) e carregamento automático de widget
document.addEventListener('DOMContentLoaded', () => {
  // Admin form submit (se existir)
  const adForm = document.getElementById('adForm');
  if (adForm) {
    adForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = {
        image_url: document.getElementById('image_url').value.trim(),
        target_url: document.getElementById('target_url').value.trim(),
        alt: document.getElementById('alt').value.trim(),
        position: document.getElementById('position').value.trim(),
        active: document.getElementById('active').checked ? 1 : 0
      };
      if (!formData.target_url || !formData.image_url) { alert('Informe a URL da imagem e o link de destino.'); return; }
      try {
        const resp = await fetch('/api/save-ad.php', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData)
        });
        const json = await resp.json();
        if (resp.ok) {
          alert('Anúncio salvo com sucesso.');
          adForm.reset();
        } else {
          alert('Erro ao salvar: ' + (json.error || resp.status));
        }
      } catch (err) {
        alert('Erro de rede: ' + err.message);
      }
    });
  }

  // Widget loader automático (elementos com data-ads="true")
  const widgetContainers = document.querySelectorAll('[data-ads="true"]');
  if (widgetContainers.length) {
    widgetContainers.forEach(async (container) => {
      const position = container.getAttribute('data-position') || '';
      try {
        const resp = await fetch('/api/get-ads.php?position=' + encodeURIComponent(position));
        if (!resp.ok) return;
        const json = await resp.json();
        if (!Array.isArray(json)) return;
        json.forEach(ad => {
          const a = document.createElement('a');
          a.href = ad.target_url;
          a.target = '_blank';
          a.rel = 'noopener noreferrer';
          a.style.display = 'inline-block';
          a.style.margin = '6px';

          const img = document.createElement('img');
          img.src = ad.image_url;
          img.alt = ad.alt || 'anúncio';
          img.style.maxWidth = '100%';
          img.style.height = 'auto';
          img.style.display = 'block';

          a.appendChild(img);
          container.appendChild(a);
        });
      } catch (err) {
        console.error('Erro ao carregar anúncios:', err);
      }
    });
  }
});
