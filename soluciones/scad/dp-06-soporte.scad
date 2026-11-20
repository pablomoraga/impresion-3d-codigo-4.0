// DP-06 · Soporte inclinado 60 x 50 x 4 mm, respaldo a 65°
// Diseño e Impresión 3D en el aula · Pablo Moraga · CC BY-NC-ND 4.0
$fn = 64;
cube([60, 50, 4]);
translate([0, 12, 3]) rotate([-25, 0, 0]) cube([60, 4, 55]);
translate([0, 0, 4]) cube([60, 3, 5]);
