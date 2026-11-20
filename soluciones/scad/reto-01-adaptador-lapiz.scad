// Reto 01 · Adaptador ergonómico triangular para lápiz
// Diseño e Impresión 3D en el aula · Pablo Moraga · CC BY-NC-ND 4.0
$fn = 64;
r = 3; c = 6.7;
difference() {
  hull() for (k = [0:2]) rotate([0, 0, 90 + k * 120]) translate([c, 0, 0]) cylinder(r = r, h = 45);
  translate([0, 0, -1]) cylinder(d = 8.2, h = 47);
}
