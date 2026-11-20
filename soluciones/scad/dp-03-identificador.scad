// DP-03 · Identificador de mochila 60 x 25 x 4 mm
// Diseño e Impresión 3D en el aula · Pablo Moraga · CC BY-NC-ND 4.0
$fn = 64;
difference() {
  hull() for (x = [3, 57], y = [3, 22]) translate([x, y, 0]) cylinder(r = 3, h = 4);
  translate([7, 12.5, -1]) cylinder(d = 6, h = 6);
}
translate([37, 12.5, 4]) linear_extrude(1) text("ALEX", size = 8, halign = "center", valign = "center", font = "Liberation Sans:style=Bold");
