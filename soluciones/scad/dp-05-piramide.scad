// DP-05 · Pirámide de Keops seccionada 50 x 50 x 35 mm
// Diseño e Impresión 3D en el aula · Pablo Moraga · CC BY-NC-ND 4.0
$fn = 64;
difference() {
  polyhedron(points = [[-25,-25,0],[25,-25,0],[25,25,0],[-25,25,0],[0,0,35]],
             faces = [[0,1,4],[1,2,4],[2,3,4],[3,0,4],[3,2,1,0]]);
  translate([0, -26, -1]) cube([26, 26, 40]);            // cuarto frontal derecho
  translate([-2, -4, 12]) cube([8, 6, 5]);               // cámara
  translate([-1.5, 0, 14]) rotate([26, 0, 0]) cube([3, 20, 3]);  // corredor
}
