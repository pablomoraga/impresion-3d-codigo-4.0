// Reto 04 · Soporte para sensor ultrasónico HC-SR04
// Diseño e Impresión 3D en el aula · Pablo Moraga · CC BY-NC-ND 4.0
$fn = 64;
difference() {
  union() {
    translate([-25, -12.5, 0]) cube([50, 25, 3]);                         // placa frontal
    translate([-25, -12.5, 0]) cube([50, 3, 23]);                         // escuadra
    for (x = [-25, 22]) translate([x, -9.5, 3]) rotate([90, 0, 90]) linear_extrude(3) polygon([[0, 0], [12, 0], [0, 12]]);
  }
  for (x = [-13, 13]) translate([x, 0, -1]) cylinder(d = 16.2, h = 5);
  for (x = [-15, 15]) translate([x, -14, 15]) rotate([-90, 0, 0]) cylinder(d = 3.2, h = 6);
}
