"""Genera los iconos pixel-art de 16 x 16 (estilo 16 bits) e inserta el bloque en src/manual.html.

Cada icono se dibuja con primitivas sobre una rejilla de 14 x 14; el script añade el contorno
oscuro, el brillo superior y la sombra inferior/derecha para dar volumen de forma coherente.
Uso: python tools/iconos16.py  (después, python tools/construir_paginas.py)
"""
import json, math, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src", "manual.html")

PAL = {"k": "#1d1f24",
       "1": "#f6a36d", "2": "#e2672e", "3": "#a8461b",   # naranja
       "4": "#ffe08a", "5": "#f2c230", "6": "#b88a10",   # amarillo
       "7": "#9fdcec", "8": "#2c9cbc", "9": "#1d6680",   # azul turquesa
       "a": "#a6e98a", "b": "#4fbf3c", "c": "#2e7d25",   # verde
       "d": "#f39a8b", "e": "#d8432f", "f": "#8e2418",   # rojo
       "g": "#ffffff", "h": "#d9dce0", "i": "#9aa0a8",   # gris claro
       "j": "#6e747c", "m": "#454a53", "n": "#24272d",   # gris oscuro
       "p": "#e8b56c", "q": "#b07a35", "r": "#6e4a1c",   # madera / latón
       "s": "#cfa6f0", "t": "#8e4bb5", "u": "#5a2b7a"}   # morado
FAM = {"2": ("1", "3"), "5": ("4", "6"), "8": ("7", "9"), "b": ("a", "c"), "e": ("d", "f"),
       "h": ("g", "i"), "q": ("p", "r"), "t": ("s", "u"), "m": ("j", "n")}
N = 14


class Ico:
    def __init__(self):
        self.g = [[None] * N for _ in range(N)]
        self.fixed = set()

    def set(self, x, y, c, fix=False):
        if 0 <= x < N and 0 <= y < N:
            self.g[y][x] = c
            if fix:
                self.fixed.add((x, y))
            else:
                self.fixed.discard((x, y))

    def rect(self, x, y, w, h, c, fix=False):
        for j in range(y, y + h):
            for i in range(x, x + w):
                self.set(i, j, c, fix)

    def circle(self, cx, cy, r, c, fix=False):
        for j in range(N):
            for i in range(N):
                if (i - cx) ** 2 + (j - cy) ** 2 <= r * r + 0.3:
                    self.set(i, j, c, fix)

    def where(self, fn, c, fix=False):
        for j in range(N):
            for i in range(N):
                if fn(i, j):
                    self.set(i, j, c, fix)

    def px(self, pts, c):
        for x, y in pts:
            self.set(x, y, c, True)

    def clear(self, pts):
        for x, y in pts:
            self.g[y][x] = None

    def render(self):
        g = self.g
        filled = lambda x, y: 0 <= x < N and 0 <= y < N and g[y][x] is not None
        inner = [row[:] for row in g]
        for y in range(N):
            for x in range(N):
                c = g[y][x]
                if c in FAM and (x, y) not in self.fixed:
                    up = filled(x, y - 1) and g[y - 1][x] in (c, FAM[c][0])
                    down = filled(x, y + 1)
                    right = filled(x + 1, y)
                    if not up:
                        inner[y][x] = FAM[c][0]
                    elif not down or not right:
                        inner[y][x] = FAM[c][1]
        out = [["."] * 16 for _ in range(16)]
        for y in range(N):
            for x in range(N):
                if inner[y][x]:
                    out[y + 1][x + 1] = inner[y][x]
        for y in range(16):
            for x in range(16):
                if out[y][x] == "." and any(0 <= x + dx < 16 and 0 <= y + dy < 16 and out[y + dy][x + dx] not in (".", "k")
                                            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    out[y][x] = "k"
        return ["".join(r) for r in out]


def icons():
    D = {}

    def new(name):
        D[name] = Ico()
        return D[name]

    a = new("bulb"); a.circle(6.5, 5, 5, "5"); a.rect(4, 10, 6, 1, "h"); a.rect(4, 11, 6, 1, "j", True); a.rect(5, 12, 4, 1, "h")
    a.px([(4, 3), (4, 4), (5, 2)], "g"); a.px([(6, 7), (7, 7), (5, 6), (8, 6)], "6"); a.px([(6, 8), (7, 8)], "6")

    a = new("printer"); a.rect(0, 0, 14, 14, "m"); a.rect(2, 2, 10, 7, "7", True); a.rect(2, 3, 10, 1, "i", True)
    a.rect(5, 2, 4, 3, "h"); a.px([(6, 5), (7, 5)], "n"); a.rect(5, 7, 4, 2, "2"); a.rect(2, 9, 10, 1, "n", True)
    a.rect(0, 10, 14, 4, "h"); a.rect(2, 11, 4, 2, "b", True); a.px([(10, 11), (11, 11)], "j")

    a = new("chest"); a.rect(0, 5, 14, 9, "q"); a.where(lambda x, y: 1 <= y <= 4 and (x - 6.5) ** 2 / 49 + (y - 5) ** 2 / 16 <= 1, "q")
    a.rect(0, 5, 14, 1, "r", True); a.rect(0, 12, 14, 1, "r", True); a.rect(2, 1, 1, 12, "6", True); a.rect(11, 1, 1, 12, "6", True)
    a.rect(5, 5, 4, 4, "5"); a.px([(6, 7), (7, 7)], "n")

    a = new("layers"); a.rect(0, 1, 14, 3, "8"); a.rect(0, 5, 14, 3, "2"); a.rect(0, 9, 14, 3, "5")
    a.px([(1, 1), (2, 1), (1, 5), (2, 5), (1, 9), (2, 9)], "g")

    a = new("pencil")
    a.where(lambda x, y: abs(x + y - 13) <= 1 and 3 <= x <= 13, "5")
    a.where(lambda x, y: abs(x + y - 13) <= 1 and x >= 11, "e")
    a.where(lambda x, y: abs(x + y - 13) <= 1 and 9 <= x <= 10, "h")
    a.where(lambda x, y: abs(x + y - 13) <= 1 and 2 <= x <= 3, "p", True)
    a.where(lambda x, y: x + y >= 12 and x + y <= 14 and x <= 1, "n", True)
    a.clear([(0, 12), (0, 14 - 1)])

    a = new("trophy"); a.rect(3, 0, 8, 6, "5"); a.rect(4, 6, 6, 1, "5"); a.rect(5, 7, 4, 1, "5"); a.rect(6, 8, 2, 3, "6", True)
    a.px([(1, 1), (1, 2), (2, 3), (2, 4), (12, 1), (12, 2), (11, 3), (11, 4)], "5"); a.rect(3, 11, 8, 3, "q"); a.rect(5, 12, 4, 1, "5", True)
    a.px([(5, 2), (5, 3), (4, 1)], "g")

    a = new("book"); a.rect(1, 0, 12, 13, "e"); a.rect(1, 0, 2, 13, "f", True); a.rect(3, 12, 10, 2, "g", True); a.rect(3, 13, 10, 1, "h", True)
    a.rect(5, 3, 6, 3, "g", True); a.rect(6, 4, 4, 1, "i", True)

    a = new("apple"); a.circle(6.5, 8, 5.4, "e"); a.clear([(6, 3), (7, 3)]); a.rect(6, 0, 1, 4, "r", True); a.px([(8, 1), (9, 1), (10, 1), (8, 2), (9, 2)], "b")
    a.px([(3, 6), (4, 5), (3, 7)], "g")

    a = new("chip"); a.rect(2, 2, 10, 10, "m")
    for k in (3, 6, 9):
        a.rect(k, 0, 2, 2, "i"); a.rect(k, 12, 2, 2, "i"); a.rect(0, k, 2, 2, "i"); a.rect(12, k, 2, 2, "i")
    a.rect(4, 4, 6, 6, "8"); a.px([(5, 5), (6, 5)], "g")

    a = new("leaf")
    a.where(lambda x, y: ((x - y) / 1.414) ** 2 / 9 + ((x + y - 13) / 1.414) ** 2 / 42 <= 1, "b")
    a.where(lambda x, y: x + y == 13 and 2 <= x <= 12, "c", True); a.px([(1, 12), (0, 13)], "r")

    a = new("column"); a.where(lambda x, y: y <= 3 and abs(x - 6.5) <= 2 + y * 1.6, "h"); a.rect(0, 4, 14, 1, "i", True)
    for k in (1, 6, 11):
        a.rect(k, 5, 2, 6, "h")
    a.rect(0, 11, 14, 3, "h")

    a = new("calc"); a.rect(1, 0, 12, 14, "m"); a.rect(3, 2, 8, 3, "a", True); a.rect(7, 3, 3, 1, "c", True)
    for j in (6, 9, 12):
        for i in (3, 6, 9):
            a.rect(i, j, 2, 1 if j == 12 else 2, "2" if (i == 9 and j == 12) else "h")

    a = new("heart"); a.where(lambda x, y: ((x - 3.5) ** 2 + (y - 3.5) ** 2 <= 11 or (x - 9.5) ** 2 + (y - 3.5) ** 2 <= 11 or (y >= 4 and abs(x - 6.5) <= 13 - y - 0.5)), "e")
    a.px([(2, 2), (3, 1), (2, 3)], "g")

    a = new("shield"); a.where(lambda x, y: (y <= 7 and 1 <= x <= 12) or (y > 7 and abs(x - 6.5) <= 5.5 - (y - 7) * 0.95), "8")
    a.px([(3, 7), (4, 8), (5, 9), (6, 8), (7, 7), (8, 6), (9, 5), (10, 4)], "g")

    a = new("warn"); a.where(lambda x, y: y >= 1 and abs(x - 6.5) <= (y - 0.5) * 0.55 + 0.5, "5"); a.rect(6, 4, 2, 5, "n", True); a.rect(6, 10, 2, 2, "n", True)

    a = new("star")
    pts = []
    for k in range(10):
        r = 7.2 if k % 2 == 0 else 3.4
        t = -math.pi / 2 + k * math.pi / 5
        pts.append((6.5 + r * math.cos(t), 7.2 + r * math.sin(t)))

    def inside(x, y):
        c = False
        for i in range(len(pts)):
            x1, y1 = pts[i]; x2, y2 = pts[i - 1]
            if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                c = not c
        return c
    a.where(lambda x, y: inside(x + 0.5, y + 0.5), "5"); a.px([(6, 3), (5, 5)], "g")

    a = new("medkit"); a.rect(4, 0, 6, 1, "m"); a.px([(4, 1), (4, 2), (9, 1), (9, 2)], "m"); a.rect(0, 3, 14, 11, "h")
    a.rect(6, 5, 2, 7, "e"); a.rect(3, 7, 8, 3, "e")

    a = new("wifi")
    for i, h in ((0, 4), (5, 8), (10, 12)):
        a.rect(i, 13 - h, 3, h + 1, "8")
    a = new("sd"); a.where(lambda x, y: 2 <= x <= 11 and not (x >= 9 and y < x - 8), "m")
    for k in (4, 6, 8):
        a.rect(k, 1, 1, 3, "p", True)
    a.rect(3, 7, 8, 5, "8", True); a.rect(4, 8, 6, 1, "7", True)

    a = new("thermo"); a.rect(5, 0, 4, 10, "h"); a.circle(6.5, 10.5, 3.2, "e"); a.rect(6, 3, 2, 7, "e", True)
    a.px([(10, 2), (10, 4), (10, 6)], "j")

    a = new("drop"); a.circle(6.5, 8.5, 4.6, "8"); a.where(lambda x, y: y <= 5 and abs(x - 6.5) <= y * 0.8, "8"); a.px([(4, 7), (4, 8), (5, 6)], "g")

    a = new("bag"); a.rect(1, 4, 12, 10, "2"); a.px([(4, 4), (4, 3), (4, 2), (5, 1), (6, 0), (7, 0), (8, 1), (9, 2), (9, 3), (9, 4)], "m")
    a.rect(4, 8, 6, 3, "g", True)

    a = new("cube")
    a.where(lambda x, y: x <= 6 and 3 + x * 0.5 <= y + 0.5 <= 10 + x * 0.5, "2", True)
    a.where(lambda x, y: x >= 7 and 3 + (13 - x) * 0.5 <= y + 0.5 <= 10 + (13 - x) * 0.5, "3", True)
    a.where(lambda x, y: abs(x - 6.5) * 0.5 + abs(y - 3.2) <= 3.3, "1", True)
    a.px([(5, 2), (6, 2)], "g")

    a = new("target"); a.circle(6.5, 6.5, 6.6, "e"); a.circle(6.5, 6.5, 4.6, "g", True); a.circle(6.5, 6.5, 2.7, "e"); a.circle(6.5, 6.5, 1, "g", True)

    a = new("nozzle"); a.rect(2, 0, 10, 5, "h"); a.rect(2, 1, 10, 1, "i", True); a.rect(2, 3, 10, 1, "i", True); a.rect(3, 5, 8, 2, "e")
    a.rect(4, 7, 6, 2, "q"); a.rect(5, 9, 4, 1, "q"); a.rect(6, 10, 2, 1, "q"); a.rect(6, 12, 2, 2, "2")

    a = new("bed"); a.rect(0, 9, 14, 3, "m"); a.rect(0, 12, 14, 2, "n", True)
    for i in range(1, 14, 3):
        a.px([(i, 10)], "j")
    for k in (2, 6, 10):
        a.px([(k, 7), (k + 1, 6), (k + 1, 5), (k, 4), (k, 3), (k + 1, 2)], "2")

    a = new("ams"); a.rect(0, 0, 14, 3, "7"); a.rect(0, 3, 14, 11, "m")
    for i, c in zip((1, 4, 7, 10), ("2", "8", "h", "5")):
        a.rect(i, 4, 3, 6, c)
    a.rect(0, 11, 14, 1, "n", True)
    for i in (2, 5, 8, 11):
        a.px([(i, 12)], "b")

    a = new("camera"); a.rect(0, 3, 14, 10, "m"); a.rect(3, 1, 5, 2, "m"); a.circle(7, 8, 3.4, "n", True); a.circle(7, 8, 2.4, "8"); a.px([(6, 7)], "g")
    a.px([(11, 4), (12, 4)], "5")

    a = new("purge"); a.where(lambda x, y: y >= 10 and abs(x - 6.5) <= 6, "2"); a.where(lambda x, y: 6 <= y <= 9 and abs(x - 6.5) <= 4.2, "8")
    a.where(lambda x, y: 2 <= y <= 5 and abs(x - 6.5) <= 2.4, "5"); a.px([(6, 0), (7, 0), (7, 1)], "e")

    a = new("spool"); a.circle(6.5, 6.5, 6.7, "m"); a.circle(6.5, 6.5, 5.2, "2"); a.circle(6.5, 6.5, 2.4, "h"); a.circle(6.5, 6.5, 1.1, "n", True)
    a.px([(3, 3), (4, 2)], "1")
    return {k: v.render() for k, v in D.items()}


def main():
    ic = icons()
    block = ("/*ICON16-INI*/\nvar ICP=" + json.dumps(PAL, separators=(",", ":")) + ";\nvar ICON16=" +
             json.dumps(ic, separators=(",", ":")).replace('],"', '],\n"') + ";\n/*ICON16-FIN*/")
    s = open(SRC, encoding="utf-8").read()
    if "/*ICON16-INI*/" in s:
        s = re.sub(r"/\*ICON16-INI\*/.*?/\*ICON16-FIN\*/", lambda m: block, s, flags=re.S)
    else:
        s = s.replace("function px(name){", block + "\nfunction px(name){", 1)
    open(SRC, "w", encoding="utf-8").write(s)
    for k, rows in ic.items():
        print(k)
        print("\n".join(rows))


if __name__ == "__main__":
    main()
