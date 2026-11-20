"""Convierte los STL de texto de soluciones/stl/ a STL binario (mucho más ligero)."""
import os, re, struct

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, "soluciones", "stl")
NUM = r"[-+0-9.eE]+"

for f in sorted(os.listdir(DIR)):
    if not f.endswith(".stl"):
        continue
    path = os.path.join(DIR, f)
    raw = open(path, "rb").read()
    if not raw[:5].lower().startswith(b"solid"):
        continue  # ya es binario
    txt = raw.decode("ascii", "ignore")
    facets = re.findall(r"facet normal\s+(%s)\s+(%s)\s+(%s)\s+outer loop\s+vertex\s+(%s)\s+(%s)\s+(%s)\s+vertex\s+(%s)\s+(%s)\s+(%s)\s+vertex\s+(%s)\s+(%s)\s+(%s)" % ((NUM,) * 12), txt)
    with open(path, "wb") as out:
        out.write(b"Diseno e Impresion 3D en el aula - Pablo Moraga".ljust(80, b" "))
        out.write(struct.pack("<I", len(facets)))
        for fc in facets:
            out.write(struct.pack("<12fH", *map(float, fc), 0))
    print(f"{f}: {len(facets)} triángulos, {len(raw)//1024} KB -> {os.path.getsize(path)//1024} KB")
