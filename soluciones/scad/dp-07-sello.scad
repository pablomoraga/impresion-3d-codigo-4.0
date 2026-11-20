// DP-07 · Sello educativo Ø 30 mm con texto en espejo
// Diseño e Impresión 3D en el aula · Pablo Moraga · CC BY-NC-ND 4.0
$fn = 64;
translate([0, 0, 1.5]) cylinder(d = 30, h = 8);
translate([0, 0, 9.5]) cylinder(d = 14, h = 25);
mirror([1, 0, 0]) linear_extrude(1.5) text("ABC", size = 8, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
