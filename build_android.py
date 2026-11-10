#!/usr/bin/env python3
"""Gera android/app/src/main/assets/index.html (app para TVs Android / Google TV)
a partir de src/budo-timer.html.

O GitHub Actions roda este script e compila o app (BudoTimer.apk) a cada mudança.
Uso local: python3 build_android.py
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, 'src', 'budo-timer.html')
OUT = os.path.join(BASE, 'android', 'app', 'src', 'main', 'assets', 'index.html')

HEAD = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
"""

def build():
    src = open(SRC, encoding='utf-8').read()
    src = src.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
    i = src.index('<style>'); j = src.index('</style>') + len('</style>')
    head, style, body = src[:i], src[i:j], src[j:]
    doc = HEAD + head + style + '\n</head>\n<body>\n' + body.strip() + '\n</body>\n</html>\n'
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write(doc)
    print('android/app/src/main/assets/index.html pronto')

if __name__ == '__main__':
    build()
