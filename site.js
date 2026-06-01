(function(){
  var doc = document, dd = doc.documentElement;

  // Dark mode toggle
  var themeBtn = doc.getElementById('theme-toggle');
  var saved = localStorage.getItem('theme');
  if (saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    dd.setAttribute('data-theme', 'dark');
  }
  if (themeBtn) {
    themeBtn.addEventListener('click', function(){
      var isDark = dd.getAttribute('data-theme') === 'dark';
      dd.setAttribute('data-theme', isDark ? 'light' : 'dark');
      localStorage.setItem('theme', isDark ? 'light' : 'dark');
    });
    var cur = dd.getAttribute('data-theme');
    themeBtn.textContent = cur === 'dark' ? '\u2600' : '\u263E';
    themeBtn.setAttribute('aria-label', cur === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
  }

  // Hamburger menu toggle
  var menuBtn = doc.querySelector('.menu-toggle');
  if (menuBtn) {
    menuBtn.addEventListener('click', function(){
      doc.querySelector('header nav').classList.toggle('open');
    });
  }

  // Email obfuscation
  doc.querySelectorAll('.eml').forEach(function(e){
    var a = e.dataset.eml + '@' + e.dataset.dom;
    e.href = 'mailto:' + a;
    e.textContent = a;
    e.removeAttribute('data-eml');
    e.removeAttribute('data-dom');
  });

  // Print button
  var printBtn = doc.getElementById('print-btn');
  if (printBtn) {
    printBtn.addEventListener('click', function(){ window.print(); });
  }

  // Glossary tooltips
  var glossaryData = typeof window.glossaryData !== 'undefined' ? window.glossaryData : null;
  if (glossaryData) {
    var terms = doc.querySelectorAll('.glossary-term');
    terms.forEach(function(el){
      var key = el.getAttribute('data-term') || el.textContent.trim().toLowerCase();
      var found = glossaryData.filter(function(g){
        return g.term.toLowerCase().indexOf(key) !== -1 || key.indexOf(g.term.toLowerCase()) !== -1;
      });
      if (found.length) {
        var tip = doc.createElement('span');
        tip.className = 'glossary-tooltip';
        tip.textContent = found[0].definition;
        el.appendChild(tip);
        el.setAttribute('tabindex', '0');
        el.setAttribute('role', 'button');
        el.setAttribute('aria-describedby', 'tip');
      }
    });
  }
})();
