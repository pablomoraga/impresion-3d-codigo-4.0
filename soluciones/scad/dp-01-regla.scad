// DP-01 · Regla escolar milimetrada 100 x 20 x 3 mm
// Diseño e Impresión 3D en el aula · Pablo Moraga · CC BY-NC-ND 4.0
$fn = 64;
cube([100, 20, 3]);
for (i = [0:10]) {
  L = (i % 5 == 0) ? 10 : 6;
  x = min(max(i * 10 - 0.4, 0), 99.2);
  translate([x, 20 - L, 3]) cube([0.8, L, 1]);
  tx = min(max(i * 10, 2.5), 97.5);
  translate([tx, 3, 3]) linear_extrude(1) text(str(i), size = 4, halign = "center", font = "Liberation Sans:style=Bold");
}
