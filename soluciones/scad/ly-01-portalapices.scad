// LY-01 · Portalápices 70 x 70 x 100 mm, pared 2 mm
// Diseño e Impresión 3D en el aula · Pablo Moraga · CC BY-NC-ND 4.0
$fn = 64;
difference() {
  linear_extrude(100) offset(r = 8) square(54, center = true);
  translate([0, 0, 2]) linear_extrude(100) offset(r = 6) square(54, center = true);
}
