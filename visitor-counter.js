(function(){
  /* ── STEP 1: Create a Firebase project at https://console.firebase.google.com ──
   * 1. Go to Firebase Console → Add project
   * 2. Project settings → General → "Your apps" → Add app → Web
   * 3. Copy the firebaseConfig object below and paste your values
   * 4. In Firebase Console → Build → Realtime Database → Create Database
   * 5. Start in test mode (or locked — rules can be tightened later)
   */
  var firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_PROJECT.firebaseapp.com",
    databaseURL: "https://YOUR_PROJECT-default-rtdb.firebaseio.com",
    projectId: "YOUR_PROJECT",
    storageBucket: "YOUR_PROJECT.firebasestorage.app",
    messagingSenderId: "YOUR_SENDER_ID",
    appId: "YOUR_APP_ID"
  };

  var doc = document;
  var totalEl = doc.getElementById('visitor-total');
  var topEl = doc.getElementById('top-visitors');
  var sectionEl = doc.querySelector('.visitor-section');
  if (!totalEl && !topEl) return;

  try {
    firebase.initializeApp(firebaseConfig);
  } catch(e) {
    if (sectionEl) sectionEl.style.display = 'none';
    return;
  }
  var db = firebase.database();
  var counterRef = db.ref('visitor-counter');

  // Unique visitor ID via localStorage
  var uuid = localStorage.getItem('cfg_visitor_id');
  if (!uuid) {
    uuid = 'v_' + Date.now().toString(36) + '_' + Math.random().toString(36).substr(2, 6);
    localStorage.setItem('cfg_visitor_id', uuid);
  }

  var visitorRef = counterRef.child('visitors/' + uuid);

  // Increment total + visitor count (transaction avoids racing)
  counterRef.child('total').transaction(function(current){
    return (current || 0) + 1;
  });
  visitorRef.child('count').transaction(function(current){
    return (current || 0) + 1;
  });
  visitorRef.child('lastVisit').set(firebase.database.ServerValue.TIMESTAMP);
  // Anonymized display name — visible to everyone
  visitorRef.child('displayName').set('Player ' + uuid.substr(-4).toUpperCase());

  // Real-time listener — updates as other visitors arrive
  counterRef.on('value', function(snapshot){
    var data = snapshot.val();
    if (!data) return;

    if (totalEl) totalEl.textContent = data.total || 0;

    // Top 5 by visit count
    var visitors = data.visitors || {};
    var sorted = Object.keys(visitors).map(function(key){
      var v = visitors[key];
      return {
        count: v.count || 0,
        name: v.displayName || 'Player ' + key.substr(-4).toUpperCase()
      };
    }).sort(function(a, b){ return b.count - a.count; }).slice(0, 5);

    if (topEl) {
      topEl.innerHTML = '';
      if (sorted.length === 0) {
        var li = doc.createElement('li');
        li.textContent = 'Be the first!';
        topEl.appendChild(li);
      } else {
        sorted.forEach(function(v, i){
          var li = doc.createElement('li');
          li.textContent = (i+1) + '. ' + v.name + ' (' + v.count + ')';
          topEl.appendChild(li);
        });
      }
    }
  });
})();
