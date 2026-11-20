"""Genera el sitio en varias páginas a partir de src/manual.html.

Uso:  python tools/construir_paginas.py
Salida: index.html, 01-por-que.html … 08-saber-mas.html, css/estilo.css y js/app.js
Edita siempre src/manual.html y vuelve a ejecutar este script.
"""
import os, re, html, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src", "manual.html")

PAGES = [
    ("index.html", ["inicio", "contenidos"], "", "Inicio"),
    ("01-por-que.html", ["porque"], "01", "¿Por qué 3D?"),
    ("02-impresora.html", ["impresora"], "02", "La impresora 3D"),
    ("03-repositorios.html", ["repositorios"], "03", "Repositorios"),
    ("04-laminador.html", ["laminador"], "04", "El laminador"),
    ("05-tinkercad.html", ["tinkercad"], "05", "Diseñar con Tinkercad"),
    ("06-layerling.html", ["layerling"], "06", "Diseñar con Layerling"),
    ("07-retos.html", ["retos"], "07", "Retos de diseño"),
    ("08-saber-mas.html", ["saber"], "08", "Para saber más"),
]
SITE = "Diseño e Impresión 3D en el aula"

EXTRA_CSS = """
/* ---- Páginas con menú lateral ---- */
.layout{display:grid;grid-template-columns:270px minmax(0,1fr);gap:32px;align-items:start;padding-top:calc(var(--offset) + 18px)}
.layout.home{padding-top:28px}
.side{position:sticky;top:calc(var(--offset) - 4px);max-height:calc(100vh - var(--offset) - 12px);overflow:auto;font-size:14px;background:var(--card);border:1.5px solid var(--ink);border-radius:12px;padding:10px 10px 12px;box-shadow:var(--shadow)}
.side-wrap>summary{display:none;font:700 12px var(--mono);text-transform:uppercase;letter-spacing:.06em;color:var(--muted);cursor:pointer;padding:6px}
.side-wrap>summary::before{content:"☰  ";color:var(--accent)}
.side-wrap[open]>summary{margin-bottom:6px}
.side-home{display:block;font:700 13px var(--mono);padding:7px 8px;border-radius:6px;color:var(--ink);text-decoration:none;margin-bottom:4px}
.side-home:hover{background:var(--bg2)}
.side-tree,.side-tree ul{list-style:none;margin:0;padding:0}
.side-tree>li>details>summary{cursor:pointer;padding:7px 8px;border-radius:6px;font-weight:700;line-height:1.3;color:var(--ink)}
.side-tree>li>details>summary:hover{background:var(--bg2)}
.side-tree>li>details[open]>summary{color:var(--ink)}
.side-tree .num{font:700 12px var(--mono);color:var(--accent);margin-right:6px}
.side-tree ul{margin:2px 0 8px 15px;border-left:2px solid var(--line);padding-left:8px}
.side-tree ul a{display:block;padding:4px 8px;border-radius:6px;color:var(--muted);text-decoration:none;font-size:13.5px;line-height:1.3}
.side-tree ul a:hover{background:var(--bg2);color:var(--ink)}
.side a.on{background:var(--ink);color:var(--bg)}
.crumbs{font:12px var(--mono);color:var(--muted);margin:0}
.crumbs a{color:var(--muted)}
.page-main .sec{padding:28px 0 8px;border-bottom:0}
.page-main .wrap{max-width:none;padding:0}
.pn{display:flex;justify-content:space-between;gap:12px;margin:32px 0 56px;flex-wrap:wrap}
.pn a{flex:1 1 260px;border:1px solid var(--line);background:var(--card);border-radius:12px;padding:14px 16px;text-decoration:none;color:var(--ink);box-shadow:var(--shadow)}
.pn a:hover{border-color:var(--accent)}
.pn a small{display:block;font:600 11px var(--mono);color:var(--muted);text-transform:uppercase;letter-spacing:.05em}
.pn a.next{text-align:right}
@media (max-width:1060px) and (min-width:760px){.layout{grid-template-columns:230px minmax(0,1fr);gap:22px}}
@media (max-width:759px){.layout{grid-template-columns:1fr;gap:12px}.side{position:static;max-height:none}.side-wrap>summary{display:block}}
"""


def strip_tags(s):
    s = re.sub(r"<small[^>]*>.*?</small>", "", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def slug(s):
    s = s.lower()
    for a, b in zip("áéíóúüñ", "aeiouun"):
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:40]


def main():
    src = open(SRC, encoding="utf-8").read()
    head = src[: src.index("</head>")]
    style = re.search(r"<style>(.*?)</style>", head, re.S).group(1)
    head = re.sub(r"<style>.*?</style>", '<link rel="stylesheet" href="css/estilo.css">', head, flags=re.S)
    top = src[src.index("<body>") + 6: src.index("<main>")]
    main_html = src[src.index("<main>") + 6: src.index("</main>")]
    s0 = src.index("<script>", src.index("</main>"))
    footer = src[src.index("</main>") + 7: s0]
    js = src[s0 + 8: src.index("</script>", s0)]

    # Secciones de primer nivel
    sections = {}
    for m in re.finditer(r'(<!--[^\n]*-->\s*)?<section class="(?:sec|hero)"[^>]*\bid="([^"]+)"', main_html):
        end = main_html.index("</section>", m.start()) + len("</section>")
        sections[m.group(2)] = main_html[m.start():end]

    # Subapartados (h3.sub) con identificador y mapa de destinos
    subs, target = {}, {}
    for fname, ids, num, title in PAGES:
        subs[fname] = []
        for sid in ids:
            body = sections[sid]
            target[sid] = (fname, "" if sid == ids[0] else sid)

            def add_id(m):
                attrs, inner = m.group(1), m.group(2)
                idm = re.search(r'\bid="([^"]+)"', attrs)
                hid = idm.group(1) if idm else slug(strip_tags(inner))
                if not idm:
                    attrs += f' id="{hid}" style="scroll-margin-top:110px"'
                subs[fname].append((hid, strip_tags(inner)))
                return f'<h3 class="sub"{attrs}>{inner}</h3>'

            body = re.sub(r'<h3 class="sub"([^>]*)>(.*?)</h3>', add_id, body, flags=re.S)
            sections[sid] = body
            for idm in re.finditer(r'\bid="([^"]+)"', body):
                target.setdefault(idm.group(1), (fname, idm.group(1)))

    # Pestañas de «Para saber más» como entradas del menú lateral
    subs["08-saber-mas.html"] += [("tab-prof", "Para el profesorado"), ("tab-lam", "Otros laminadores"),
                                   ("tab-rec", "Recursos"), ("tab-cred", "Créditos y licencias")]

    def relink(chunk, current):
        def rep(m):
            x = m.group(1)
            if x not in target:
                return m.group(0)
            f, frag = target[x]
            if f == current:
                return f'href="#{frag}"' if frag else f'href="{f}"'
            return f'href="{f}' + (f"#{frag}" if frag else "") + '"'
        return re.sub(r'href="#([^"]+)"', rep, chunk)

    os.makedirs(os.path.join(ROOT, "css"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "js"), exist_ok=True)
    css_txt, js_txt = style.strip() + "\n" + EXTRA_CSS, js.strip() + "\n"
    open(os.path.join(ROOT, "css", "estilo.css"), "w", encoding="utf-8").write(css_txt)
    open(os.path.join(ROOT, "js", "app.js"), "w", encoding="utf-8").write(js_txt)
    # Marca de versión: obliga al navegador a descargar los archivos nuevos tras cada cambio
    ver = hashlib.md5((css_txt + js_txt).encode("utf-8")).hexdigest()[:8]
    head = head.replace('href="css/estilo.css"', f'href="css/estilo.css?v={ver}"')

    top = top.replace('href="#contenidos">Saltar al índice', 'href="#contenido">Saltar al contenido')

    for i, (fname, ids, num, title) in enumerate(PAGES):
        page_title = SITE if fname == "index.html" else f"{num} · {title} · {SITE}"
        h = re.sub(r"<title>.*?</title>", f"<title>{html.escape(page_title)}</title>", head, flags=re.S)
        content = "\n".join(sections[s] for s in ids)
        # Menú lateral en árbol (estilo «Scratch en el aula»): todos los apartados y sus subapartados
        tree = []
        for f2, _ids, n2, t2 in PAGES[1:]:
            cur = f2 == fname
            items = [f'<li><a href="{f2}"' + (' class="on" aria-current="page"' if cur else "") + '>Presentación</a></li>']
            for hid, t in subs[f2]:
                href = f"#{hid}" if cur else f"{f2}#{hid}"
                items.append(f'<li><a href="{href}" data-sub="{hid}">{html.escape(t)}</a></li>')
            tree.append(f'<li><details{" open" if cur else ""}><summary><span class="num">{n2}</span>{html.escape(t2)}</summary><ul>{"".join(items)}</ul></details></li>')
        home_on = ' class="side-home on" aria-current="page"' if fname == "index.html" else ' class="side-home"'
        side_html = (f'<nav class="side" aria-label="Índice del manual"><details class="side-wrap" open><summary>Índice del manual</summary>'
                     f'<a href="index.html"{home_on}>Inicio</a><ul class="side-tree">{"".join(tree)}</ul></details></nav>\n')
        if fname == "index.html":
            body = (f'<main id="contenido">\n{sections["inicio"]}\n<div class="wrap layout home">\n{side_html}'
                    f'<div class="page-main">\n{sections["contenidos"]}\n</div>\n</div>\n</main>')
        else:
            prev = PAGES[i - 1] if i > 0 else None
            nxt = PAGES[i + 1] if i + 1 < len(PAGES) else None
            pn = '<nav class="pn" aria-label="Página anterior y siguiente">'
            if prev:
                pn += f'<a class="prev" href="{prev[0]}"><small>← Anterior</small>{(prev[2] + " · ") if prev[2] else ""}{html.escape(prev[3])}</a>'
            if nxt:
                pn += f'<a class="next" href="{nxt[0]}"><small>Siguiente →</small>{nxt[2]} · {html.escape(nxt[3])}</a>'
            pn += "</nav>"
            body = (f'<main id="contenido">\n<div class="wrap layout">\n{side_html}'
                    f'<div class="page-main">\n<p class="crumbs"><a href="index.html">Inicio</a> › {num} · {html.escape(title)}</p>\n{content}\n{pn}\n</div>\n</div>\n</main>')
        out = (h + "</head>\n" + f'<body data-page="{fname}">' + relink(top, fname) + relink(body, fname) +
               relink(footer, fname) + f'<script src="js/app.js?v={ver}"></script>\n</body>\n</html>\n')
        open(os.path.join(ROOT, fname), "w", encoding="utf-8").write(out)
        print(f"{fname}: {len(out)//1024} KB · {len(subs[fname])} subapartados")


if __name__ == "__main__":
    main()
