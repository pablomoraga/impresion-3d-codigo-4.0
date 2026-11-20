// Reto 05 · Medalla en tres niveles (2 · 3,5 · 5 mm)
// Diseño e Impresión 3D en el aula · Pablo Moraga · CC BY-NC-ND 4.0
$fn = 64;
cylinder(d = 65, h = 2);
difference() { cylinder(d = 65, h = 3.5); translate([0, 0, -1]) cylinder(d = 57, h = 6); }
linear_extrude(5) polygon([for (i = [0:9]) let(r = i % 2 ? 8 : 20, t = 90 + i * 36) [r * cos(t), r * sin(t)]]);
translate([0, 35.5, 0]) difference() { cylinder(d = 13, h = 3); translate([0, 0, -1]) cylinder(d = 5, h = 5); }
