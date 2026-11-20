// DP-04 · Dado de 25 mm con puntos rehundidos
// Diseño e Impresión 3D en el aula · Pablo Moraga · CC BY-NC-ND 4.0
$fn = 64;
$fn = 32;
s = 25; r = 2; d = 6.5;
function pips(n) = n == 1 ? [[0,0]] : n == 2 ? [[-d,-d],[d,d]] : n == 3 ? [[-d,-d],[0,0],[d,d]] :
  n == 4 ? [[-d,-d],[-d,d],[d,-d],[d,d]] : n == 5 ? [[-d,-d],[-d,d],[0,0],[d,-d],[d,d]] :
  [[-d,-d],[-d,0],[-d,d],[d,-d],[d,0],[d,d]];
module face(n) for (p = pips(n)) translate([p[0], p[1], s/2 + 0.5]) sphere(r = 2.5);
translate([0, 0, s/2]) difference() {
  hull() for (x = [-1,1], y = [-1,1], z = [-1,1]) translate([x, y, z] * (s/2 - r)) sphere(r = r);
  face(1);
  rotate([180, 0, 0]) face(6);
  rotate([0, 90, 0]) face(2);
  rotate([0, -90, 0]) face(5);
  rotate([-90, 0, 0]) face(3);
  rotate([90, 0, 0]) face(4);
}
