(function () {
  function $(sel) { return document.querySelector(sel); }
  function $$(sel) { return Array.prototype.slice.call(document.querySelectorAll(sel)); }

  // Show everything fully before printing or capturing
  function prepare() {
    $$('.fill[data-level]').forEach(function (f) { f.style.width = f.dataset.level + '%'; });
    var t = $('#typing');
    if (t && t.dataset.text) t.textContent = t.dataset.text;
  }

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement('script');
      s.src = src;
      s.onload = resolve;
      s.onerror = function () { reject(new Error('Could not load ' + src)); };
      document.head.appendChild(s);
    });
  }

  // html2canvas can't do object-fit, so draw photos as cropped backgrounds instead
  function fixPhotos(doc) {
    Array.prototype.slice.call(doc.querySelectorAll('img.avatar, .photo img')).forEach(function (img) {
      if (!img.src) return;
      var box = doc.createElement('div');
      box.className = img.className;
      box.style.display = 'block';
      box.style.backgroundImage = 'url("' + img.src + '")';
      box.style.backgroundSize = 'cover';
      box.style.backgroundPosition = 'center';
      box.style.backgroundRepeat = 'no-repeat';
      if (!img.classList.contains('avatar')) {
        // gallery photos fill their square box; the avatar keeps its size from the CSS
        box.style.width = '100%';
        box.style.height = '100%';
      }
      img.parentNode.replaceChild(box, img);
    });
  }

  var printBtn = $('#print-btn');
  if (printBtn) {
    printBtn.addEventListener('click', function () {
      prepare();
      window.print();
    });
  }

  var dlBtn = $('#download-btn');
  if (dlBtn) {
    dlBtn.addEventListener('click', function () {
      var target = $('.profile-theme');
      var original = dlBtn.textContent;
      dlBtn.textContent = 'Preparing...';
      dlBtn.disabled = true;
      prepare();

      var cdn = 'https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js';
      var ready = window.html2canvas
        ? Promise.resolve()
        : loadScript(dlBtn.dataset.lib).catch(function () { return loadScript(cdn); });

      ready.then(function () {
        return window.html2canvas(target, {
          scale: 2,
          useCORS: true,
          backgroundColor: getComputedStyle(document.body).backgroundColor,
          ignoreElements: function (el) { return el.classList && el.classList.contains('no-print'); },
          onclone: fixPhotos
        });
      }).then(function (canvas) {
        var a = document.createElement('a');
        a.download = (dlBtn.dataset.filename || 'my-profile') + '.png';
        a.href = canvas.toDataURL('image/png');
        document.body.appendChild(a);
        a.click();
        a.remove();
      }).catch(function (err) {
        alert('Could not create the image: ' + (err && err.message ? err.message : err) +
              '\n\nUse Print / Save as PDF instead.');
      }).then(function () {
        dlBtn.textContent = original;
        dlBtn.disabled = false;
      });
    });
  }
})();