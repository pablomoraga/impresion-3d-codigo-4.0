"""Escribe los modelos OpenSCAD de las soluciones en soluciones/scad/.

Uso:  python tools/soluciones_scad.py
Después: tools/generar_stl.ps1 convierte cada .scad en .stl con OpenSCAD.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "soluciones", "scad")
HEAD = "// {t}\n// Diseño e Impresión 3D en el aula · Pablo Moraga · CC BY-NC-ND 4.0\n$fn = 64;\n"

M = {}

M["dp-01-regla"] = ("DP-01 · Regla escolar milimetrada 100 x 20 x 3 mm", """
cube([100, 20, 3]);
for (i = [0:10]) {
  L = (i % 5 == 0) ? 10 : 6;
  x = min(max(i * 10 - 0.4, 0), 99.2);
  translate([x, 20 - L, 3]) cube([0.8, L, 1]);
  tx = min(max(i * 10, 2.5), 97.5);
  translate([tx, 3, 3]) linear_extrude(1) text(str(i), size = 4, halign = "center", font = "Liberation Sans:style=Bold");
}
""")

M["dp-02-moneda"] = ("DP-02 · Moneda histórica Ø 35 x 3 mm con bisel", """
cylinder(d = 35, h = 2.3);
translate([0, 0, 2.3]) cylinder(d1 = 35, d2 = 33.6, h = 0.7);
translate([0, 0, 3]) linear_extrude(1) text("X", size = 14, halign = "center", valign = "center", font = "Liberation Serif:style=Bold");
""")

M["dp-03-identificador"] = ("DP-03 · Identificador de mochila 60 x 25 x 4 mm", """
difference() {
  hull() for (x = [3, 57], y = [3, 22]) translate([x, y, 0]) cylinder(r = 3, h = 4);
  translate([7, 12.5, -1]) cylinder(d = 6, h = 6);
}
translate([37, 12.5, 4]) linear_extrude(1) text("ALEX", size = 8, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
""")

M["dp-04-dado"] = ("DP-04 · Dado de 25 mm con puntos rehundidos", """
$fn = 32;
s = 25; r = 2; d = 6.5;
function pips(n) = n == 1 ? [[0,0]] : n == 2 ? [[-d,-d],[d,d]] : n == 3 ? [[-d,-d],[0,0],[d,d]] :
  n == 4 ? [[-d,-d],[-d,d],[d,-d],[d,d]] : n == 5 ? [[-d,-d],[-d,d],[0,0],[d,-d],[d,d]] :
  [[-d,-d],[-d,0],[-d,d],[d,-d],[d,0],[d,d]];
module face(n) for (p = pips(n)) translate([p[0], p[1], s/2 + 0.5]) sphere(r = 2.5);
translate([0, 0, s/2]) difference() {
  hull() for (x = [-1,1], y = [-1,1], z = [-1,1]) translate([x, y, z] * (s/2 - r)) sphere(r = r);
  face(1);
  rotate([180, 0, 0]) face(6);
  rotate([0, 90, 0]) face(2);
  rotate([0, -90, 0]) face(5);
  rotate([-90, 0, 0]) face(3);
  rotate([90, 0, 0]) face(4);
}
""")

M["dp-05-piramide"] = ("DP-05 · Pirámide de Keops seccionada 50 x 50 x 35 mm", """
difference() {
  polyhedron(points = [[-25,-25,0],[25,-25,0],[25,25,0],[-25,25,0],[0,0,35]],
             faces = [[0,1,4],[1,2,4],[2,3,4],[3,0,4],[3,2,1,0]]);
  translate([0, -26, -1]) cube([26, 26, 40]);            // cuarto frontal derecho
  translate([-2, -4, 12]) cube([8, 6, 5]);               // cámara
  translate([-1.5, 0, 14]) rotate([26, 0, 0]) cube([3, 20, 3]);  // corredor
}
""")

M["dp-06-soporte"] = ("DP-06 · Soporte inclinado 60 x 50 x 4 mm, respaldo a 65°", """
cube([60, 50, 4]);
translate([0, 12, 3]) rotate([-25, 0, 0]) cube([60, 4, 55]);
translate([0, 0, 4]) cube([60, 3, 5]);
""")

M["dp-07-sello"] = ("DP-07 · Sello educativo Ø 30 mm con texto en espejo", """
translate([0, 0, 1.5]) cylinder(d = 30, h = 8);
translate([0, 0, 9.5]) cylinder(d = 14, h = 25);
mirror([1, 0, 0]) linear_extrude(1.5) text("ABC", size = 8, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
""")

M["dp-08-braille"] = ("DP-08 · Ficha táctil en braille: AULA", """
$fn = 24;
cube([40, 30, 3]);
cells = [[1], [1,3,6], [1,2,3], [1]];   // A U L A
x0 = (40 - (3 * 6 + 2.5)) / 2;
function dot(n) = [ (n > 3 ? 2.5 : 0), [17.5, 15, 12.5][(n - 1) % 3] ];
for (c = [0:3]) for (n = cells[c]) translate([x0 + c * 6 + dot(n)[0], dot(n)[1], 3]) scale([1, 1, 0.8]) sphere(r = 0.75);
""")

M["dp-09-media-molecula-h2o"] = ("DP-09 · Media molécula de agua (imprimir dos y unir)", """
a = 52.25; L = 22;
intersection() {
  union() {
    sphere(d = 20);
    for (s = [-1, 1]) {
      p = [s * L * sin(a), -L * cos(a), 0];
      hull() { sphere(d = 4); translate(p) sphere(d = 4); }
      translate(p) sphere(d = 12);
    }
  }
  translate([-50, -50, 0]) cube([100, 100, 50]);
}
""")

M["dp-10-base-remezcla"] = ("DP-10 · Base Ø 50 x 4 mm para remezclas (con figura de ejemplo)", """
cylinder(d = 50, h = 4);
// Figura de ejemplo: sustituir por el modelo importado
translate([0, 4, 3.5]) linear_extrude(15) polygon([for (i = [0:9]) let(r = i % 2 ? 7 : 16, t = 90 + i * 36) [r * cos(t), r * sin(t)]]);
translate([0, -17, 4]) linear_extrude(1) text("3.º B", size = 5, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
""")

M["reto-01-adaptador-lapiz"] = ("Reto 01 · Adaptador ergonómico triangular para lápiz", """
r = 3; c = 6.7;
difference() {
  hull() for (k = [0:2]) rotate([0, 0, 90 + k * 120]) translate([c, 0, 0]) cylinder(r = r, h = 45);
  translate([0, 0, -1]) cylinder(d = 8.2, h = 47);
}
""")

M["reto-02-volcan-seccion"] = ("Reto 02 · Volcán en sección (cara de corte sobre la placa)", """
module volcan() difference() {
  union() {
    translate([-45, -45, 0]) cube([90, 90, 4]);
    rotate_extrude() polygon([[0,4],[45,4],[38,12],[28,26],[18,42],[10,55],[7,59],[0,59]]);
  }
  translate([0, 0, 49]) cylinder(d1 = 0, d2 = 16, h = 11);        // cráter
  translate([0, 0, 18]) cylinder(d = 6, h = 40);                 // chimenea
  translate([0, 0, 14]) scale([15, 15, 6]) sphere(r = 1);        // cámara magmática
}
rotate([90, 0, 0]) difference() { volcan(); translate([-50, -50, -1]) cube([100, 50, 70]); }
""")

M["reto-03-reloj-sol"] = ("Reto 03 · Reloj de sol horizontal para latitud 37°", """
phi = 37;
cylinder(d = 100, h = 4);
for (h = [-6:6]) {
  th = abs(h) == 6 ? 90 : atan(sin(phi) * tan(abs(h) * 15));
  ang = h < 0 ? th : -th;                                // mañana al oeste (−X)
  rotate([0, 0, ang]) translate([-0.75, 40, 4]) cube([1.5, 10, 1]);
}
translate([1.5, 0, 4]) rotate([0, -90, 0]) linear_extrude(3) polygon([[0, 0], [0, 50], [50 * tan(phi), 50]]);
""")

M["reto-04-soporte-hcsr04"] = ("Reto 04 · Soporte para sensor ultrasónico HC-SR04", """
difference() {
  union() {
    translate([-25, -12.5, 0]) cube([50, 25, 3]);                         // placa frontal
    translate([-25, -12.5, 0]) cube([50, 3, 23]);                         // escuadra
    for (x = [-25, 22]) translate([x, -9.5, 3]) rotate([90, 0, 90]) linear_extrude(3) polygon([[0, 0], [12, 0], [0, 12]]);
  }
  for (x = [-13, 13]) translate([x, 0, -1]) cylinder(d = 16.2, h = 5);
  for (x = [-15, 15]) translate([x, -14, 15]) rotate([-90, 0, 0]) cylinder(d = 3.2, h = 6);
}
""")

M["reto-05-medalla"] = ("Reto 05 · Medalla en tres niveles (2 · 3,5 · 5 mm)", """
cylinder(d = 65, h = 2);
difference() { cylinder(d = 65, h = 3.5); translate([0, 0, -1]) cylinder(d = 57, h = 6); }
linear_extrude(5) polygon([for (i = [0:9]) let(r = i % 2 ? 8 : 20, t = 90 + i * 36) [r * cos(t), r * sin(t)]]);
translate([0, 35.5, 0]) difference() { cylinder(d = 13, h = 3); translate([0, 0, -1]) cylinder(d = 5, h = 5); }
""")

M["ly-01-portalapices"] = ("LY-01 · Portalápices 70 x 70 x 100 mm, pared 2 mm", """
difference() {
  linear_extrude(100) offset(r = 8) square(54, center = true);
  translate([0, 0, 2]) linear_extrude(100) offset(r = 6) square(54, center = true);
}
""")

M["ly-04-esfera-reloj"] = ("LY-04 · Esfera de reloj Ø 90 x 3 mm con texto en arco", """
cylinder(d = 90, h = 3);
for (k = [0:11]) rotate([0, 0, k * 30]) translate([-1, 35, 3]) cube([2, 8, 1.5]);
txt = "CEIP AULA 3D"; n = len(txt); step = 11;
for (i = [0:n - 1]) rotate([0, 0, (n - 1) / 2 * step - i * step]) translate([0, 26, 3]) linear_extrude(1.2) text(txt[i], size = 5, halign = "center", font = "Liberation Sans:style=Bold");
""")

M["ly-06-regla-40cm-dividida"] = ("LY-06 · Regla de 400 mm en dos mitades con cola de milano", """
g = 0.2;                                     // holgura
module cola(e = 0) linear_extrude(4 + (e > 0 ? 2 : 0)) polygon([[0, -3 - e], [8 + e, -5 - e], [8 + e, 5 + e], [0, 3 + e]]);
module marcas(x0) for (i = [0:20]) translate([i * 10 - 0.4 + (i == 0 ? 0.4 : 0) - (i == 20 ? 0.4 : 0), 30 - ((i + x0) % 5 == 0 ? 10 : 6), 4]) cube([0.8, (i + x0) % 5 == 0 ? 10 : 6, 1]);
// Mitad A: 0–200 mm con saliente
cube([200, 30, 4]); translate([200, 15, 0]) cola(); marcas(0);
// Mitad B: 200–400 mm con hueco (impresa al lado)
translate([0, 40, 0]) difference() {
  union() { cube([200, 30, 4]); marcas(0); }
  translate([-0.01, 15, -1]) cola(g);
}
""")


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, (title, body) in M.items():
        open(os.path.join(OUT, name + ".scad"), "w", encoding="utf-8").write(HEAD.format(t=title) + body.lstrip("\n"))
    print(len(M), "modelos en", OUT)


if __name__ == "__main__":
    main()
