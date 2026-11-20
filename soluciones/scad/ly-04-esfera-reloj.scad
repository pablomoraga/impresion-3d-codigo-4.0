// LY-04 · Esfera de reloj Ø 90 x 3 mm con texto en arco
// Diseño e Impresión 3D en el aula · Pablo Moraga · CC BY-NC-ND 4.0
$fn = 64;
cylinder(d = 90, h = 3);
for (k = [0:11]) rotate([0, 0, k * 30]) translate([-1, 35, 3]) cube([2, 8, 1.5]);
txt = "CEIP AULA 3D"; n = len(txt); step = 11;
for (i = [0:n - 1]) rotate([0, 0, (n - 1) / 2 * step - i * step]) translate([0, 26, 3]) linear_extrude(1.2) text(txt[i], size = 5, halign = "center", font = "Liberation Sans:style=Bold");
