// public/js/ads-widget.js
// Widget leve (alternativa se você preferir um arquivo separado)
(function(){
  document.addEventListener('DOMContentLoaded', function(){
    var containers = document.querySelectorAll('[data-ads="true"]');
    if (!containers.length) return;
    containers.forEach(function(container){
      var pos = container.getAttribute('data-position') || '';
      fetch('/api/get-ads.php?position=' + encodeURIComponent(pos)).then(function(resp){
        if (!resp.ok) return;
        return resp.json();
      }).then(function(list){
        if (!Array.isArray(list)) return;
        list.forEach(function(ad){
          var a = document.createElement('a');
          a.href = ad.target_url;
          a.target = '_blank';
          a.rel = 'noopener noreferrer';
          a.style.display = 'inline-block';
          a.style.margin = '6px';

          var img = document.createElement('img');
          img.src = ad.image_url;
          img.alt = ad.alt || '';
          img.style.maxWidth = '100%';
          img.style.height = 'auto';
          a.appendChild(img);
          container.appendChild(a);
        });
      }).catch(function(e){ console.error(e); });
    });
  });
})();
