/* BUDO Timer: funciona sem internet depois da primeira abertura */
var CACHE = 'budo-timer-8831a03f64';
var FILES = ['./', './index.html', './manifest.webmanifest', './icon-192.png', './icon-512.png', './apple-touch-icon.png'];
self.addEventListener('install', function(e){
  e.waitUntil(caches.open(CACHE).then(function(c){ return c.addAll(FILES); }).then(function(){ return self.skipWaiting(); }));
});
self.addEventListener('activate', function(e){
  e.waitUntil(caches.keys().then(function(keys){
    return Promise.all(keys.filter(function(k){ return k !== CACHE; }).map(function(k){ return caches.delete(k); }));
  }).then(function(){ return self.clients.claim(); }));
});
self.addEventListener('fetch', function(e){
  if (e.request.method !== 'GET') return;
  /* Página: tenta a versão nova primeiro, cai para a guardada sem internet */
  if (e.request.mode === 'navigate') {
    e.respondWith(fetch(e.request).then(function(r){
      var copy = r.clone(); caches.open(CACHE).then(function(c){ c.put('./index.html', copy); }); return r;
    }).catch(function(){ return caches.match('./index.html'); }));
    return;
  }
  /* Ícones e fontes: usa o que já está guardado */
  e.respondWith(caches.match(e.request).then(function(hit){
    return hit || fetch(e.request).then(function(r){
      var copy = r.clone(); caches.open(CACHE).then(function(c){ c.put(e.request, copy); }); return r;
    });
  }));
});
