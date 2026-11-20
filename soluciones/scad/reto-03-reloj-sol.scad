// Reto 03 · Reloj de sol horizontal para latitud 37°
// Diseño e Impresión 3D en el aula · Pablo Moraga · CC BY-NC-ND 4.0
$fn = 64;
phi = 37;
cylinder(d = 100, h = 4);
for (h = [-6:6]) {
  th = abs(h) == 6 ? 90 : atan(sin(phi) * tan(abs(h) * 15));
  ang = h < 0 ? th : -th;                                // mañana al oeste (−X)
  rotate([0, 0, ang]) translate([-0.75, 40, 4]) cube([1.5, 10, 1]);
}
translate([1.5, 0, 4]) rotate([0, -90, 0]) linear_extrude(3) polygon([[0, 0], [0, 50], [50 * tan(phi), 50]]);
