// DP-10 · Base Ø 50 x 4 mm para remezclas (con figura de ejemplo)
// Diseño e Impresión 3D en el aula · Pablo Moraga · CC BY-NC-ND 4.0
$fn = 64;
cylinder(d = 50, h = 4);
// Figura de ejemplo: sustituir por el modelo importado
translate([0, 4, 3.5]) linear_extrude(15) polygon([for (i = [0:9]) let(r = i % 2 ? 7 : 16, t = 90 + i * 36) [r * cos(t), r * sin(t)]]);
translate([0, -17, 4]) linear_extrude(1) text("3.º B", size = 5, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
