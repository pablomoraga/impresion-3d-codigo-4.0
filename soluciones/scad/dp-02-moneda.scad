// DP-02 · Moneda histórica Ø 35 x 3 mm con bisel
// Diseño e Impresión 3D en el aula · Pablo Moraga · CC BY-NC-ND 4.0
$fn = 64;
cylinder(d = 35, h = 2.3);
translate([0, 0, 2.3]) cylinder(d1 = 35, d2 = 33.6, h = 0.7);
translate([0, 0, 3]) linear_extrude(1) text("X", size = 14, halign = "center", valign = "center", font = "Liberation Serif:style=Bold");
