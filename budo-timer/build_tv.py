#!/usr/bin/env python3
"""Gera tizen/index.html (app Samsung Tizen) a partir de src/budo-timer.html.

TVs Samsung antigas (Tizen 5.0, 2019) usam um Chromium antigo que não entende
clamp(), min(), max(), env() nem gap em flexbox. Este script:
  1. coloca antes de cada declaração com essas funções uma versão fixa
     calculada para a tela da TV (1920x1080); navegadores novos usam a original,
     os antigos ignoram a original e ficam com a fixa;
  2. acrescenta grid-gap nas grades;
  3. cria margens de substituição para o gap de flexbox, ativadas só quando um
     teste no carregamento mostra que o navegador não suporta gap em flex.

Uso: python3 build_tv.py   (rodar na pasta principal do projeto)
"""
import re, sys, os

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, 'src', 'budo-timer.html')
OUT = os.path.join(BASE, 'tizen', 'index.html')
VW, VH = 19.2, 10.8   # 1% da largura e da altura numa tela 1920x1080

FN = r'(?<![a-z-])(clamp|min|max)\('

def to_px(tok):
    tok = tok.strip()
    m = re.fullmatch(r'(-?[\d.]+)(px|vw|vh)?', tok)
    if not m:
        return None
    n, u = float(m.group(1)), m.group(2) or 'px'
    return n * {'px': 1, 'vw': VW, 'vh': VH}[u]

def evaluate(expr):
    """Troca clamp/min/max/env por um único valor válido em navegadores antigos."""
    expr = re.sub(r'env\([^()]*\)', 'ENV', expr)
    pat = re.compile(r'(?<![a-z-])(clamp|min|max)\(([^()]*)\)')
    while True:
        m = pat.search(expr)
        if not m:
            break
        fn, args = m.group(1), [a.strip() for a in m.group(2).split(',')]
        vals = [to_px(a) for a in args]
        if fn == 'clamp':
            lo, mid, hi = vals
            if mid is not None and lo <= mid <= hi:
                pick = args[1]
            else:
                pick = args[0] if (mid is None or mid < lo) else args[2]
        else:
            known = [(v, a) for v, a in zip(vals, args) if v is not None]
            pick = (min if fn == 'min' else max)(known)[1]
        expr = expr[:m.start()] + pick + expr[m.end():]
    return expr

def add_fallbacks(css):
    decl = re.compile(r'([{;]\s*)([a-z-]+)(\s*:\s*)([^;{}]*' + FN + r'[^;{}]*)')
    # Substitui de vez (não deixa a versão original): numa TV antiga, uma regra com
    # var() é aceita na leitura e só falha na hora de aplicar, apagando a reserva.
    return decl.sub(lambda m: f"{m.group(1)}{m.group(2)}{m.group(3)}{evaluate(m.group(4))}", css)

def gap_rules(css):
    """Margens de substituição para gap em flexbox + grid-gap nas grades."""
    extra = []
    for sel, body in re.findall(r'([^{}]+)\{([^{}]*)\}', css):
        sel = re.sub(r'/\*.*?\*/', '', sel, flags=re.S).strip()
        if not sel or sel.startswith('@'):
            continue
        g = re.search(r'(?:^|;)\s*gap\s*:\s*([^;]+)', body)
        if not g:
            continue
        gap = evaluate(g.group(1)).strip()
        if 'display:grid' in body.replace(' ', ''):
            continue
        if 'display:flex' not in body.replace(' ', ''):
            continue
        prop = 'margin-top' if 'flex-direction:column' in body.replace(' ', '') else 'margin-left'
        for s in sel.split(','):
            extra.append(f".no-fgap {s.strip()}>*+*{{{prop}:{gap}}}")
    extra.append(".no-fgap .preset>.key+*{margin-top:0}")
    extra.append(".no-fgap .brand i{margin-right:.6em}")
    extra.append(".no-fgap .dot{margin-right:.4em}")
    extra.append(".no-fgap .top>.setup{margin-left:auto}")
    css = re.sub(r'(display:grid;[^{}]*?)gap:([^;}]+)', lambda m: m.group(1) + 'grid-gap:' + evaluate(m.group(2)) + ';gap:' + m.group(2), css)
    return css + '\n/* Sem gap em flexbox (TVs antigas) */\n' + '\n'.join(extra) + '\n'

DETECT = """<script>
/* TVs antigas não suportam gap em flexbox: liga as margens de substituição */
(function(){try{var d=document.createElement('div');d.style.display='flex';d.style.flexDirection='column';d.style.rowGap='1px';
d.appendChild(document.createElement('div'));d.appendChild(document.createElement('div'));document.documentElement.appendChild(d);
var ok=d.scrollHeight===1;d.parentNode.removeChild(d);if(!ok)document.documentElement.className+=' no-fgap';}catch(e){}})();
</script>
"""

def build(simulate_old=None):
    src = open(SRC, encoding='utf-8').read()
    i = src.index('<style>'); j = src.index('</style>') + len('</style>')
    head, style, body = src[:i], src[i:j], src[j:]
    css = style[len('<style>'):-len('</style>')]
    css = gap_rules(add_fallbacks(css))
    head = head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
    doc = ('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
           + head + '<script type="text/javascript" src="$WEBAPIS/webapis/webapis.js"></script>\n'
           + '<style>' + css + '</style>\n' + DETECT + '</head>\n<body>\n' + body.strip() + '\n</body>\n</html>\n')
    open(OUT, 'w', encoding='utf-8').write(doc)
    if simulate_old:
        # Simula o navegador antigo: apaga tudo o que ele ignoraria
        old = re.sub(r';?[a-z-]+\s*:[^;{}]*(' + FN + r'|env\()[^;{}]*', '', css)
        old = re.sub(r'(display:flex;[^{}]*?);?gap:[^;}]+', r'\1', old)
        old = re.sub(r'([{;])gap:[^;}]+', r'\1', old)
        sim = doc.replace('<style>' + css + '</style>', '<style>' + old + '</style>')
        sim = sim.replace("if(!ok)document.documentElement.className+=' no-fgap';", "document.documentElement.className+=' no-fgap';")
        open(simulate_old, 'w', encoding='utf-8').write(sim)

if __name__ == '__main__':
    build(sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == '--simulate-old' else None)
    print('ok')
