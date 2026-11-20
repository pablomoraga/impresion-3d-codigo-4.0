// LY-06 · Regla de 400 mm en dos mitades con cola de milano
// Diseño e Impresión 3D en el aula · Pablo Moraga · CC BY-NC-ND 4.0
$fn = 64;
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
