(function(){
  var doc = document, dd = doc.documentElement;

  // Dark mode toggle
  var themeBtn = doc.getElementById('theme-toggle');
  var saved = localStorage.getItem('theme');
  if (saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    dd.setAttribute('data-theme', 'dark');
  }
  if (themeBtn) {
    var cur = dd.getAttribute('data-theme');
    var themeIcon = doc.getElementById('theme-icon');
    if (themeIcon) {
      themeIcon.textContent = cur === 'dark' ? '\u2600' : '\u263E';
    }
    themeBtn.setAttribute('aria-label', cur === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
    themeBtn.addEventListener('click', function(){
      var isDark = dd.getAttribute('data-theme') === 'dark';
      dd.setAttribute('data-theme', isDark ? 'light' : 'dark');
      localStorage.setItem('theme', isDark ? 'light' : 'dark');
      if (themeIcon) {
        themeIcon.textContent = isDark ? '\u2600' : '\u263E';
      }
      themeBtn.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
    });
  }

  // Hamburger menu toggle
  var menuBtn = doc.querySelector('.menu-toggle');
  if (menuBtn) {
    menuBtn.addEventListener('click', function(){
      doc.querySelector('header nav').classList.toggle('open');
    });
  }

  // Dropdown keyboard accessibility
  doc.querySelectorAll('.dropdown > .dropbtn').forEach(function(btn){
    btn.setAttribute('role', 'button');
    btn.setAttribute('aria-haspopup', 'true');
    var dd = btn.parentElement;
    var isOpen = false;
    btn.setAttribute('aria-expanded', 'false');

    function openDropdown() {
      isOpen = true;
      btn.setAttribute('aria-expanded', 'true');
      dd.classList.add('is-open');
    }
    function closeDropdown() {
      isOpen = false;
      btn.setAttribute('aria-expanded', 'false');
      dd.classList.remove('is-open');
    }

    btn.addEventListener('click', function(e){
      e.preventDefault();
      if (isOpen) { closeDropdown(); } else { openDropdown(); }
    });
    btn.addEventListener('keydown', function(e){
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        if (isOpen) { closeDropdown(); } else { openDropdown(); }
      }
      if (e.key === 'Escape' && isOpen) {
        closeDropdown();
        btn.focus();
      }
    });
    // Close on click outside
    doc.addEventListener('click', function(e){
      if (isOpen && !dd.contains(e.target)) { closeDropdown(); }
    });
  });

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

  // Back-to-top button
  var backBtn = doc.getElementById('back-to-top');
  if (backBtn) {
    var scrollThreshold = 300;
    doc.addEventListener('scroll', function(){
      if (dd.scrollTop > scrollThreshold || doc.body.scrollTop > scrollThreshold) {
        backBtn.classList.add('visible');
      } else {
        backBtn.classList.remove('visible');
      }
    }, { passive: true });
    backBtn.addEventListener('click', function(){
      dd.scrollTo({ top: 0, behavior: 'smooth' });
    });
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
