#!/usr/bin/env python3
"""Gera a pasta docs/ (versão do celular) a partir de src/budo-timer.html.

A pasta docs/ é o que o GitHub Pages publica. Ela vira um app instalável
(PWA): ícone na tela inicial, tela cheia deitada e funcionamento sem internet.

Uso: python3 build_web.py   (rodar na pasta principal do projeto)
"""
import hashlib, json, os

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, 'src', 'budo-timer.html')
OUT = os.path.join(BASE, 'docs')
ICONS = os.path.join(BASE, 'tizen', 'icon.png')

HEAD = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#202124">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="BUDO Timer">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-192.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
"""

REGISTER = """<script>
/* Guarda o app no celular para abrir sem internet */
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function(){ navigator.serviceWorker.register('sw.js').catch(function(){}); });
}
/* Mantém deitado quando o celular deixa (Android, app instalado) */
try { if (screen.orientation && screen.orientation.lock) screen.orientation.lock('landscape').catch(function(){}); } catch(e) {}
</script>
"""

SW = """/* BUDO Timer: funciona sem internet depois da primeira abertura */
var CACHE = 'budo-timer-%s';
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
"""

def build():
    src = open(SRC, encoding='utf-8').read()
    src = src.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
    i = src.index('<style>'); j = src.index('</style>') + len('</style>')
    head, style, body = src[:i], src[i:j], src[j:]
    doc = HEAD + head + style + '\n' + REGISTER + '</head>\n<body>\n' + body.strip() + '\n</body>\n</html>\n'
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(doc)

    version = hashlib.sha1(doc.encode('utf-8')).hexdigest()[:10]
    open(os.path.join(OUT, 'sw.js'), 'w', encoding='utf-8').write(SW % version)

    manifest = {
        'name': 'BUDO Timer', 'short_name': 'BUDO Timer',
        'description': 'Timer de rounds para jiu-jitsu.',
        'lang': 'pt-BR', 'start_url': './', 'scope': './',
        'display': 'fullscreen', 'orientation': 'landscape',
        'background_color': '#202124', 'theme_color': '#202124',
        'icons': [
            {'src': 'icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
            {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
            {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'}
        ]
    }
    open(os.path.join(OUT, 'manifest.webmanifest'), 'w', encoding='utf-8').write(json.dumps(manifest, ensure_ascii=False, indent=2))

    try:
        from PIL import Image
        im = Image.open(ICONS).convert('RGB')
        for name, size in [('icon-192.png', 192), ('icon-512.png', 512), ('apple-touch-icon.png', 180)]:
            im.resize((size, size), Image.LANCZOS).save(os.path.join(OUT, name))
    except ImportError:
        print('Aviso: instale o Pillow (pip install pillow) para gerar os ícones.')
    print('docs/ pronto (versão ' + version + ')')

if __name__ == '__main__':
    build()
