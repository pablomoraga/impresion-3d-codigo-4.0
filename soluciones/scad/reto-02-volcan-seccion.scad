// Reto 02 · Volcán en sección (cara de corte sobre la placa)
// Diseño e Impresión 3D en el aula · Pablo Moraga · CC BY-NC-ND 4.0
$fn = 64;
module volcan() difference() {
  union() {
    translate([-45, -45, 0]) cube([90, 90, 4]);
    rotate_extrude() polygon([[0,4],[45,4],[38,12],[28,26],[18,42],[10,55],[7,59],[0,59]]);
  }
  translate([0, 0, 49]) cylinder(d1 = 0, d2 = 16, h = 11);        // cráter
  translate([0, 0, 18]) cylinder(d = 6, h = 40);                 // chimenea
  translate([0, 0, 14]) scale([15, 15, 6]) sphere(r = 1);        // cámara magmática
}
rotate([90, 0, 0]) difference() { volcan(); translate([-50, -50, -1]) cube([100, 50, 70]); }
